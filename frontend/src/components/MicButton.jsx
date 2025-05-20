'use client'
// components/MicButton.jsx
export default function MicButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-red-600 text-white px-4 py-2 rounded"
    >
      🎤 Talk
    </button>
  )
}


