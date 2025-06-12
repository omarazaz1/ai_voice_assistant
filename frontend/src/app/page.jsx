'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { motion } from 'framer-motion'
import FloatingMic from '@/components/FloatingMic'
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
            setMessages(prev => [...prev, { from: 'ai', text: ' Could not get response.' }])
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
            console.error('Microphone error:', err)
            setMessages(prev => [...prev, { from: 'ai', text: 'Microphone access failed.' }])
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
            setMessages(prev => [...prev, { from: 'ai', text: 'Voice processing failed.' }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-pink-500 p-4">
            <div className="max-w-2xl mx-auto space-y-6 bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-6">
                <div className="text-center space-y-1">
                    <h1 className="text-4xl font-bold text-gray-900">AI Voice Assistant</h1>
                    <p className="text-lg text-gray-700">Talk or type to get real-time answers from your AI.</p>
                </div>

                <Card className="h-[24rem] overflow-y-auto">
                    <CardContent className="p-4">
                        <ChatBox messages={messages} />
                    </CardContent>
                </Card>

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
                            <Button
                                variant="outline"
                                onClick={() => {
                                    setMessages([])
                                    localStorage.removeItem('chatHistory')
                                }}
                                className="w-full sm:w-auto"
                            >
                                Clear
                            </Button>
                        </div>

                        <div className="flex justify-end mt-2">
                            <FloatingMic onClick={startRecording} isRecording={isRecording} />
                        </div>

                        {isRecording && <p className="text-sm text-yellow-600 text-right">🎤 Recording...</p>}
                        {loading && <Loader />}
                    </CardContent>
                </Card>

                <audio id="responseAudio" controls className="w-full mt-2" />
            </div>
        </div>
    )
}
