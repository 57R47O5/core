import "./contact.css"
import * as Icons from "react-icons/fa";

export default function ContactButtons() {
  return (
    <div className="contact-floating">
      <a
        href="https://wa.me/595971312951"
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp"
      >
        <Icons.FaWhatsapp size={30} />
      </a>

      <a
        href="mailto:info@logosoft.com.py"
        className="email"
      >
        <Icons.FaEnvelope size={30} />
      </a>
    </div>
  )
}