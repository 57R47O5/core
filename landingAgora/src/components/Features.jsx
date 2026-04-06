import "./features.css"

const features = [
  {
    title: "Geolocalización",
    desc: "Visualizá votantes en mapa",
    img: "/images/map.png",
  },
  {
    title: "Segmentación",
    desc: "Clasificá por intención de voto",
    img: "/images/segment.png",
  },
  {
    title: "Reportes",
    desc: "Tomá decisiones con datos reales",
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