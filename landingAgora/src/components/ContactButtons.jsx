import "./contact.css"

export default function ContactButtons() {
  return (
    <div className="contact-floating">
      <a
        href="https://wa.me/59571312951"
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp"
      >
        WhatsApp
      </a>

      <a
        href="mailto:info@logosoft.com.py"
        className="email"
      >
        Email
      </a>
    </div>
  )
}