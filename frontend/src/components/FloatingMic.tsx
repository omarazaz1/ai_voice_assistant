'use client'

import React from 'react'

interface FloatingMicProps {
    onClick: () => void
    isRecording: boolean
}

const FloatingMic: React.FC<FloatingMicProps> = ({ onClick, isRecording }) => {
    return (
        <button
            onClick={onClick}
            className={`p-3 rounded-full shadow-md transition duration-300 
        ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-green-600 hover:bg-green-700'} 
        text-white text-xl`}
            aria-label="Start voice input"
        >
            🎤
        </button>
    )
}

export default FloatingMic
