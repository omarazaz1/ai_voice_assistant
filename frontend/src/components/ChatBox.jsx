'use client'

import { useEffect, useRef } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

export default function ChatBox({ messages }) {
    const chatRef = useRef(null)

    useEffect(() => {
        if (chatRef.current) {
            chatRef.current.scrollTop = chatRef.current.scrollHeight
        }
    }, [messages])

    return (
        <div
            ref={chatRef}
            className="h-80 overflow-y-auto space-y-4 pr-2"
        >
            {messages.map((msg, idx) => (
                <div
                    key={idx}
                    className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                    <Card
                        className={`max-w-[75%] ${msg.from === 'user'
                            ? 'bg-blue-100 text-right'
                            : 'bg-green-100 text-left'
                            }`}
                    >
                        <CardContent className="flex items-start gap-2 p-3">
                            {msg.from !== 'user' && (
                                <Avatar className="h-6 w-6">
                                    <AvatarFallback>🤖</AvatarFallback>
                                </Avatar>
                            )}

                            <div className="text-sm leading-relaxed">
                                {msg.text}
                                <span className="block text-xs text-muted-foreground mt-1">
                                    {new Date().toLocaleTimeString()}
                                </span>
                            </div>

                            {msg.from === 'user' && (
                                <Avatar className="h-6 w-6">
                                    <AvatarFallback>👤</AvatarFallback>
                                </Avatar>
                            )}
                        </CardContent>
                    </Card>
                </div>
            ))}
        </div>
    )
}
