import "./features.css"

const features = [
  {
    title: "Geolocalización",
    desc: "Donde están los votantes",
    img: "images/visita.png",
  },
  {
    title: "Segmentación",
    desc: "Quiénes te quieren votar",
    img: "images/segmentacion.png",
  },
  {
    title: "Reportes",
    desc: "Qué quieren tus votantes",
    img: "images/visitas-listadas.png",
  },
]

export default function Features() {
  return (
    <section className="features">
      {features.map((f, i) => (
        <div key={i} className="card">
         <img src={f.img} alt={f.title} className="feature-img" />
          <h3>{f.title}</h3>
          <p>{f.desc}</p>
        </div>
      ))}
    </section>
  )
}