import assert from 'node:assert/strict'
import { test } from 'node:test'
import { appendDemoExchange, createConversation, createDemoExchange } from './conversation.ts'

test('new conversations have independent identities and histories', () => {
  const first = createConversation()
  const second = createConversation()

  assert.notEqual(first.id, second.id)
  assert.notEqual(first.messages, second.messages)
  assert.equal(first.title, 'Nouvelle conversation')
  assert.deepEqual(first.messages, [])
})

test('the first message names the conversation and later messages preserve its title and history', () => {
  const original = createConversation()
  const firstExchange = createDemoExchange('Consulter mes comptes')
  const first = appendDemoExchange(original, firstExchange)
  const secondExchange = createDemoExchange('Afficher les opérations')
  const second = appendDemoExchange(first, secondExchange)

  assert.equal(first.title, 'Consulter mes comptes')
  assert.equal(second.title, first.title)
  assert.deepEqual(second.messages, [...firstExchange, ...secondExchange])
  assert.equal(original.title, 'Nouvelle conversation')
  assert.deepEqual(original.messages, [])
  assert.deepEqual(first.messages, [...firstExchange])
})

test('file-only messages use the filename as the title and explain that the file was not uploaded', () => {
  const exchange = createDemoExchange('', 'relevé.pdf')
  const conversation = appendDemoExchange(createConversation(), exchange)

  assert.equal(conversation.title, 'relevé.pdf')
  assert.equal(exchange[0].attachmentName, 'relevé.pdf')
  assert.equal(exchange[0].text, '')
  assert.ok(exchange[1].text.includes('Le fichier n’a pas été envoyé.'))
})

test('a message with text and a file uses the text as its title', () => {
  const conversation = appendDemoExchange(
    createConversation(),
    createDemoExchange('Analyser ce relevé', 'relevé.pdf'),
  )

  assert.equal(conversation.title, 'Analyser ce relevé')
})

test('text exchanges retain multiline content and clearly identify the disconnected banking demo', () => {
  const text = 'Première ligne\nDeuxième ligne'
  const [message, reply] = createDemoExchange(text)

  assert.equal(message.role, 'user')
  assert.equal(message.text, text)
  assert.equal(message.attachmentName, undefined)
  assert.equal(reply.role, 'assistant')
  assert.notEqual(message.id, reply.id)
  assert.ok(reply.text.includes('Le service bancaire n’est pas connecté'))
})
