
'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import MicButton from '@/components/MicButton'
import ChatBox from '@/components/ChatBox'
import Loader from '@/components/Loader'

export default function ChatPage() {
    const [messages, setMessages] = useState([])
    const [userInput, setUserInput] = useState('')
    const [isRecording, setIsRecording] = useState(false)
    const [loading, setLoading] = useState(false)
    const mediaRecorderRef = useRef(null)
    const chunksRef = useRef([])

    useEffect(() => {
        const stored = localStorage.getItem('chatHistory')
        if (stored) setMessages(JSON.parse(stored))
    }, [])

    useEffect(() => {
        localStorage.setItem('chatHistory', JSON.stringify(messages))
    }, [messages])

    const handleSendMessage = async () => {
        if (!userInput.trim()) return
        const question = userInput.trim()
        setMessages(prev => [...prev, { from: 'user', text: question }])
        setUserInput('')
        setLoading(true)

        try {
            const res = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, user_id: 'guest' }),
            })
            const data = await res.json()
            setMessages(prev => [...prev, { from: 'ai', text: data.response }])
        } catch {
            setMessages(prev => [...prev, { from: 'ai', text: '⚠️ Could not get response.' }])
        } finally {
            setLoading(false)
        }
    }

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            const mediaRecorder = new MediaRecorder(stream)
            mediaRecorderRef.current = mediaRecorder
            chunksRef.current = []

            mediaRecorder.ondataavailable = e => chunksRef.current.push(e.data)
            mediaRecorder.onstop = async () => {
                const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
                await sendAudioToBackend(blob)
            }

            mediaRecorder.start()
            setIsRecording(true)

            setTimeout(() => {
                mediaRecorder.stop()
                setIsRecording(false)
            }, 5000)
        } catch (err) {
            console.error('🎤 Microphone error:', err)
            setMessages(prev => [...prev, { from: 'ai', text: '⚠️ Microphone access failed.' }])
        }
    }

    const sendAudioToBackend = async (blob) => {
        setLoading(true)
        const formData = new FormData()
        formData.append('file', blob, 'voice.webm')

        try {
            const res = await fetch('http://127.0.0.1:8000/voice-chat/', {
                method: 'POST',
                body: formData,
            })

            const data = await res.json()
            setMessages(prev => [...prev, { from: 'ai', text: data.response }])

            const audioRes = await fetch('http://127.0.0.1:8000/audio')
            if (!audioRes.ok) return
            const audioBlob = await audioRes.blob()
            const audioUrl = URL.createObjectURL(audioBlob)

            const player = document.getElementById("responseAudio")
            if (player) {
                player.pause()
                player.src = audioUrl
                player.load()
                player.play()
            }
        } catch {
            setMessages(prev => [...prev, { from: 'ai', text: '⚠️ Voice processing failed.' }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="p-4 md:p-6 max-w-2xl mx-auto space-y-6">
            <h1 className="text-2xl md:text-3xl font-bold">🎙️ Talk or Type to Your Assistant</h1>

            {/* Chat Area */}
            <Card className="h-[24rem] overflow-y-auto">
                <CardContent className="p-4">
                    <ChatBox messages={messages} />
                </CardContent>
            </Card>

            {/* Input + Controls */}
            <Card>
                <CardContent className="p-4 space-y-4">
                    <div className="flex gap-2 flex-col sm:flex-row">
                        <Input
                            placeholder="Ask a question..."
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                            className="flex-1"
                        />
                        <Button onClick={handleSendMessage} className="w-full sm:w-auto">Send</Button>
                    </div>

                    <MicButton onClick={startRecording} />
                    {isRecording && <p className="text-sm text-yellow-600">🎤 Recording...</p>}
                    {loading && <Loader />}
                </CardContent>
            </Card>

            <audio id="responseAudio" controls className="w-full mt-2" />
        </div>
    )
}
