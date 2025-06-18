import express from 'express'
import { OAuth2Client } from 'google-auth-library'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const PORT = 3000
const client = new OAuth2Client(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    process.env.GOOGLE_REDIRECT_URI
)

app.get('/', (req, res) => {
    const url = client.generateAuthUrl({
        access_type: 'offline',
        scope: ['email', 'profile', 'openid'],
    })
    res.send(`<a href="${url}">Login com Google</a>`)
})

// app.get('/callback', async (req, res) => {
//     try {
//         const { code } = req.query
//         const { tokens } = await client.getToken(code)
//         client.setCredentials(tokens)
//         const ticket = await client.verifyIdToken({
//             idToken: tokens.id_token,
//             audience: process.env.GOOGLE_CLIENT_ID,
//         })
//         const payload = ticket.getPayload()
//         const name = encodeURIComponent(payload.name)
//         const email = encodeURIComponent(payload.email)
//         // Redireciona para a página de boas-vindas com parâmetros
//         res.redirect(`/welcome?name=${name}&email=${email}`)
//     } catch (error) {
//         console.error('Erro na autenticação:', error)
//         res.status(500).send('Erro ao autenticar com o Google.')
//     }
// })

app.get('/callback', async (req, res) => {
    try {
        const { code } = req.query
        const { tokens } = await client.getToken(code)
        console.log('Tokens recebidos do Google:', tokens)
        client.setCredentials(tokens)
        const ticket = await client.verifyIdToken({
            idToken: tokens.id_token,
            audience: process.env.GOOGLE_CLIENT_ID,
        })
        const payload = ticket.getPayload()
        res.send(`Olá, ${payload.name}!`)
    } catch (error) {
        console.error('Erro na autenticação:', error)
        res.status(500).send('Erro ao autenticar com o Google.')
    }
})

app.get('/welcome', (req, res) => {
    const { name, email } = req.query
    res.send(`
        <h1>Bem-vindo, ${name}!</h1>
        <p>Seu e-mail: ${email}</p>
    `)
})

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`)
})