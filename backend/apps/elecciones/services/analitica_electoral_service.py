import re
from collections import Counter
from django.db.models import Count, Sum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from apps.elecciones.models.visita import Visita

class AnaliticaElectoralService():

    STOPWORDS = [
        "de", "la", "el", "y", "en", "a", "los", "las",
        "un", "una", "que", "con", "por", "para",
        "del", "al", "se", "su"
    ]
    
    @classmethod
    def obtener_datos_analitica(cls):
        visitas = Visita.objects.all()
        visitas_acumuladas_por_fecha = visitas.extra({'fecha': "date(fecha)"}).values('fecha').annotate(count=Count('id')).order_by('fecha')
        total_visitas = visitas.count()
        suma_resultados_visita = visitas.aggregate(total=Sum('resultado_id'))
        resultado_promedio = float(suma_resultados_visita['total']) / total_visitas if total_visitas > 0 else 0
        notas = visitas.exclude(notas__isnull=True).exclude(notas__exact="").values_list("notas", flat=True)
        wordcloud_data = cls.generar_wordcloud(notas)
        temas = cls.detectar_temas(notas)
        
        return {
            'total_visitas': total_visitas,
            'visitas_acumuladas_por_fecha': list(visitas_acumuladas_por_fecha),
            'resultado_promedio': resultado_promedio,
            'wordcloud': wordcloud_data,
            'temas': temas
        }

    
    @classmethod
    def generar_wordcloud(cls, notas):

        palabras = []

        for nota in notas:
            texto = limpiar_texto(nota)

            tokens = texto.split()

            palabras.extend(
                t for t in tokens
                if len(t) > 3 and t not in cls.STOPWORDS
            )

        conteo = Counter(palabras)

        top = conteo.most_common(50)

        total = sum(count for _, count in top)

        if total == 0:
            return []

        factor = 2000 / total

        return [
            {
                "text": palabra,
                "value": int(count * factor)
            }
            for palabra, count in top
        ]

    @classmethod
    def detectar_temas(cls,notas, n_topics=5):

        textos = [limpiar_texto(n) for n in notas if n]

        vectorizer = CountVectorizer(
            stop_words=cls.STOPWORDS,
            min_df=3
        )

        try:
            X = vectorizer.fit_transform(textos)
        except ValueError as e:
            print(f"Error al transformar los textos: {e}")
            return []

        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42
        )

        lda.fit(X)

        palabras = vectorizer.get_feature_names_out()

        temas = []

        for topic_idx, topic in enumerate(lda.components_):

            top_words = [
                palabras[i]
                for i in topic.argsort()[:-10:-1]
            ]

            temas.append({
                "tema": topic_idx,
                "palabras": top_words
            })

        return temas


def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto

