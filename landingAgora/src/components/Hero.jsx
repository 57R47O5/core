import { useEffect, useState } from "react"
import "./hero.css"

export default function Hero() {
  const targetDate = new Date("2026-10-04T07:00:00")

  const [daysLeft, setDaysLeft] = useState(0)
  const [votesPerDay, setVotesPerDay] = useState(0)

  useEffect(() => {
    const updateCountdown = () => {
      const now = new Date()
      const diff = targetDate - now

      const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

      setDaysLeft(days > 0 ? days : 0)
      setVotesPerDay(days > 0 ? Math.ceil(3203 / days) : 3203)
    }

    updateCountdown()
    const interval = setInterval(updateCountdown, 1000 * 60 * 60) // cada hora

    return () => clearInterval(interval)
  }, [])

  return (
    <section className="hero">
      <h1>Gestioná tu campaña electoral</h1>

      <p className="hero-sub">
        En Asunción, en 2021, se necesitaron al menos <strong>3203 votos</strong> para ser concejal.
      </p>

      <div className="hero-stats">
        <div>
          <span className="big">{daysLeft}</span>
          <span>días restantes</span>
        </div>

        <div>
          <span className="big">{votesPerDay}</span>
          <span>votos por día</span>
        </div>
      </div>

      <p className="hero-copy">
        Los votos no se ganan en internet.<br />
        Se ganan en la calle.<br />
        <strong>Necesitás inteligencia territorial.</strong>
      </p>

      <a
        href="https://demo.logosoft.com.py"
        className="hero-btn"
        target="_blank"
        rel="noopener noreferrer"
      >
        Empezar ahora
      </a>
    </section>
  )
}