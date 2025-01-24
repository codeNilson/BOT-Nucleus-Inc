const express = require('express')
const { Client, GatewayIntentBits } = require('discord.js')
const { DateTime } = require('luxon')
const axios = require('axios')
require('dotenv').config()

const app = express()
const port = 3000

const DISCORD_TOKEN = process.env.DISCORD_TOKEN

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent],
})

// Função para converter data e hora no formato "DD/MM/YYYY HH:mm"
function parseDateTime(input) {
  try {
    const [datePart, timePart] = input.split(" ")
    const [day, month, year] = datePart.split("/").map(Number)
    const [hour, minute] = timePart.split(":").map(Number)

    // Criar o DateTime no timezone "America/Sao_Paulo"
    const dateTime = DateTime.fromObject(
      { year, month, day, hour, minute },
      { zone: "America/Sao_Paulo" }
    )

    if (!dateTime.isValid) {
      throw new Error("Data inválida. Certifique-se de usar o formato DD/MM/YYYY HH:mm.")
    }

    return dateTime.toUTC().toISO() // Converte para UTC no formato ISO
  } catch (error) {
    throw new Error("Erro ao interpretar a data/hora. Use o formato DD/MM/YYYY HH:mm.")
  }
}

client.once('ready', () => {
  console.log(`Bot está online como ${client.user.tag}!`)
})

// Função para criar evento no Discord e Calendar
client.on('messageCreate', async (message) => {
  if (!message.content.startsWith('!createEvent') || message.author.bot) return

  const args = message.content.trim().split('|')
  args.shift()

  // Limpar os espaços em todos os argumentos
  const cleanedArgs = args.map(arg => arg.trim())

  if (cleanedArgs.length < 5) {
    return message.reply(
      'Por favor, forneça os argumentos no formato correto:\n`!createEvent | Título | Descrição | Data e Hora | ID do Canal | Emails separados por vírgula`'
    )
  }

  const [title, description, dateTime, channelId, emails] = cleanedArgs

  // Validação de entrada
  if (!title || !description || !dateTime || !channelId || !emails) {
    return message.reply(
      'Informações incompletas. Certifique-se de fornecer todos os campos necessários no formato especificado.'
    )
  }

  try {
    // Criar o evento no Discord
    const guild = message.guild

    // Converter a data e hora
    const scheduledStartTime = parseDateTime(dateTime)

    const event = await guild.scheduledEvents.create({
      name: title,
      description: description,
      scheduledStartTime: scheduledStartTime,
      privacyLevel: 2, // 1 = Público, 2 = Privado
      entityType: 2, // Tipo "voice" (evento no canal de voz)
      channel: channelId,
    })

    // Gerar o link do evento
    const discordEventLink = `https://discord.com/events/${guild.id}/${event.id}`

    // Criar o evento no Calendar
    const emailsArray = emails.split(',')
    await sendToCalendar(emailsArray, title, description, scheduledStartTime, discordEventLink)

    // Responder no Discord com o link do evento criado
    message.reply(`🎉 Evento criado com sucesso!\n📅 Link do evento no Discord: ${discordEventLink}`)
  } catch (error) {
    console.error(error)
    message.reply('❌ Ocorreu um erro ao criar o evento. Verifique os detalhes e tente novamente.')
  }
})

async function getZohoAccessToken()
{
  try {
    const clientId = process.env.ZOHO_CLIENT_ID
    const clientSecret = process.env.ZOHO_CLIENT_SECRET
    const redirectUri = process.env.ZOHO_REDIRECT_URI
    const refreshToken = process.env.ZOHO_REFRESH_TOKEN
  
    const response = await axios.post(`https://accounts.zoho.com/oauth/v2/token?refresh_token=${refreshToken}&client_id=${clientId}&client_secret=${clientSecret}&redirect_uri=${redirectUri}&grant_type=refresh_token&scope=ZohoCalendar.event.ALL`)
  
    return response.data.access_token
  } catch (error) {
    console.error(error)
    throw new Error('Erro ao obter o token de acesso.')
  }
}

// Função fictícia para enviar o evento ao Calendar
async function sendToCalendar(emails, title, description, dateTime, discordEventLink) {
  try {
    const calendarId = process.env.ZOHO_CALENDAR_UID
    console.log(calendarId)
    const token = await getZohoAccessToken()

    // Converter o dateTime para o formato exigido (start)
    const startDate = new Date(dateTime)

    // Adicionar 1 hora ao horário de início para o término
    const endDate = new Date(startDate.getTime() + 60 * 60 * 1000)

    // Formatar as datas no padrão requerido
    const formatZohoDate = (date) => {
      return DateTime.fromJSDate(date, { zone: "America/Sao_Paulo" })
        .toFormat("yyyyMMdd'T'HHmmss'Z'")
    }

    const zohoEvent = {
      "reminders": [
         {
            "action": "popup",
            "minutes": -60
         }
      ],
      "dateandtime": {
         "timezone": "America/Sao_Paulo",
         "start": formatZohoDate(startDate),
         "end": formatZohoDate(endDate)
      },
      "title": title,
      "attendees": emails.map(email => ({ email, status: "NEEDS-ACTION" })),
      "richtext_description": description + `: \n\nLink do evento no Discord: ${discordEventLink}`,
      "conference": "none"
   }

   const response = await axios.post(`https://calendar.zoho.com/api/v1/calendars/${calendarId}/events?eventdata=${encodeURIComponent(JSON.stringify(zohoEvent))}`, null, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
   })

   return response.data
  } catch (ex) {
    console.error(ex.response.data)
    throw new Error('Erro ao enviar o evento para o calendário.')
  }
}

client.login(DISCORD_TOKEN)

app.get('/callback',  async (req, res) => {
  res.send('Autorizado')
})

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`)
})