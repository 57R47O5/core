import "./features.css"

const features = [
  {
    title: "Geolocalización",
    desc: "Donde están los votantes",
    img: "/images/map.png",
  },
  {
    title: "Segmentación",
    desc: "Quiénes te quieren votar",
    img: "/images/segment.png",
  },
  {
    title: "Reportes",
    desc: "Qué quieren tus votantes",
    img: "/images/reports.png",
  },
]

export default function Features() {
  return (
    <section className="features">
      {features.map((f, i) => (
        <div key={i} className="card">
          <h3>{f.title}</h3>
          <p>{f.desc}</p>
        </div>
      ))}
    </section>
  )
}