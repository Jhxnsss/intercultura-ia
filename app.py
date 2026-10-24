import streamlit as st

st.set_page_config(page_title="Intercultura IA", page_icon="🌐", layout="wide")

SCENARIOS = {
    "Negociación comercial": {
        "context": "Una empresa colombiana quiere exportar café a una empresa japonesa. Deben acordar pedido inicial, precio y entrega.",
        "role": "Representante de compras de una empresa japonesa",
        "turns": [
            ("Gracias por la propuesta. ¿Qué volumen inicial podrían suministrar y qué precio orientativo ofrecen?", "Volumen y precio"),
            ("El precio está por encima de nuestro presupuesto. ¿Qué alternativa podrían ofrecer sin comprometer la calidad?", "Manejo de objeciones"),
            ("Podríamos empezar con un pedido de prueba. ¿Qué plazo de entrega y seguimiento propones?", "Condiciones de entrega"),
            ("Para cerrar, resume el volumen, el plazo y el siguiente paso que propones.", "Cierre y resumen"),
        ],
        "phrases": ["Thank you for your proposal.", "Could we discuss the delivery terms?", "I understand your concern.", "Would you consider a trial order?"],
    },
    "Reunión intercultural": {
        "context": "Un equipo internacional debe coordinar un proyecto con diferencias en la forma de expresar desacuerdos y tomar decisiones.",
        "role": "Coordinador/a de un equipo internacional",
        "turns": [
            ("Antes de decidir, ¿cuál es tu principal preocupación sobre la fecha límite del proyecto?", "Expresar preocupaciones"),
            ("Algunas personas interpretaron tu mensaje de otra manera. ¿Cómo podrías aclararlo respetuosamente?", "Aclarar un malentendido"),
            ("Podemos reducir el alcance o ampliar el plazo. ¿Cuál opción recomiendas y por qué?", "Justificar una propuesta"),
            ("Resume la decisión y la siguiente acción de cada integrante.", "Confirmar acuerdos"),
        ],
        "phrases": ["Could you clarify what you mean?", "I see your point of view.", "May I suggest an alternative?", "Let's agree on the next steps."],
    },
    "Resolución de desacuerdo": {
        "context": "Dos empresas no están de acuerdo con el plazo de entrega. Debes explicar tu posición y proponer una alternativa respetuosa.",
        "role": "Socio/a comercial internacional",
        "turns": [
            ("Nos preocupa que sea difícil cumplir la fecha de entrega propuesta. ¿Cuál es tu opinión?", "Explicar la posición"),
            ("¿Podrías proponer un acuerdo intermedio que considere las necesidades de ambas empresas?", "Proponer un compromiso"),
            ("¿Qué condición haría que esta alternativa fuera aceptable para ambas partes?", "Negociar condiciones"),
            ("Terminemos confirmando la nueva fecha y quién hará seguimiento.", "Cerrar el acuerdo"),
        ],
        "phrases": ["I understand your concern.", "Could we find a compromise?", "One possible solution is...", "Shall we confirm the revised deadline?"],
    },
}

def make_turns(scenario, language):
    turns = SCENARIOS[scenario]["turns"]
    if language == "Español":
        return turns
    # Versión en inglés para el prototipo
    en = {
        "Negociación comercial": [
            ("Thank you for the proposal. What initial volume could you supply, and what price do you suggest?", "Volume and price"),
            ("The price is above our budget. What alternative could you offer without compromising quality?", "Handling objections"),
            ("We could begin with a trial order. What delivery timeline and follow-up do you propose?", "Delivery terms"),
            ("To close, summarize the volume, timeline, and next step you propose.", "Closing summary"),
        ],
        "Reunión intercultural": [
            ("Before deciding, what is your main concern about the project deadline?", "Expressing concerns"),
            ("Some team members interpreted your message differently. How could you clarify it respectfully?", "Clarifying a misunderstanding"),
            ("We can reduce the scope or extend the deadline. Which option do you recommend, and why?", "Justifying a proposal"),
            ("Summarize the decision and the next action for each team member.", "Confirming agreements"),
        ],
        "Resolución de desacuerdo": [
            ("We are concerned the proposed delivery date may be difficult to meet. What is your view?", "Explaining a position"),
            ("Could you suggest a compromise that considers both companies' needs?", "Proposing a compromise"),
            ("What condition would make this alternative acceptable to both sides?", "Negotiating conditions"),
            ("Let's finish by confirming the new deadline and who will follow up.", "Closing the agreement"),
        ],
    }
    return en[scenario]

if "session" not in st.session_state:
    st.session_state.session = None

st.title("🌐 Intercultura IA")
st.caption("Prototipo académico · Simulador de negociación intercultural")

with st.sidebar:
    st.header("Configurar práctica")
    scenario = st.selectbox("Escenario", list(SCENARIOS.keys()))
    language = st.selectbox("Idioma de práctica", ["Español", "Inglés"])
    level = st.selectbox("Nivel orientativo", ["Inicial", "Intermedio", "Avanzado"], index=1)
    st.caption("El nivel es orientativo; esta versión no adapta automáticamente la dificultad.")
    if st.button("Iniciar nueva simulación", use_container_width=True):
        st.session_state.session = {
            "scenario": scenario, "language": language, "level": level,
            "turns": make_turns(scenario, language), "step": 0, "history": [],
            "feedback": None, "finished": False, "survey": None
        }
        st.rerun()
    if st.session_state.session and st.button("Reiniciar sesión", use_container_width=True):
        st.session_state.session = None
        st.rerun()

if not st.session:
    st.info("Elige escenario, idioma y nivel en la barra lateral y pulsa Iniciar nueva simulación.")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Idiomas**\n\nFormula propuestas y preguntas.")
    c2.markdown("**Comunicación intercultural**\n\nAclara mensajes y reconoce perspectivas.")
    c3.markdown("**Negociación**\n\nResponde a objeciones y resume acuerdos.")
else:
    s = st.session_state.session
    info = SCENARIOS[s["scenario"]]
    main, side = st.columns([1.65, 1])
    with main:
        st.subheader("Sala de negociación")
        st.write("**Contexto:**", info["context"])
        st.write("**Contraparte:**", info["role"])
        st.write(f"**Idioma:** {s['language']} · **Nivel:** {s['level']}")
        st.progress(min(s["step"], len(s["turns"])) / len(s["turns"]),
                    text=f"Progreso: {min(s['step'], len(s['turns']))} de {len(s['turns'])} rondas")
        for item in s["history"]:
            with st.chat_message(item["role"]):
                st.write(item["content"])

        if not s["finished"]:
            prompt, stage = s["turns"][s["step"]]
            st.markdown(f"**Ronda {s['step'] + 1}: {stage}**")
            st.info(prompt)
            with st.form(key=f"answer_form_{s['step']}"):
                answer = st.text_area("Tu respuesta", key=f"answer_{s['step']}", placeholder="Escribe tu propuesta o respuesta...", height=110)
                submitted = st.form_submit_button("Enviar respuesta")
            if submitted:
                if not answer.strip():
                    st.warning("Escribe una respuesta antes de continuar.")
                else:
                    s["history"].append({"role": "user", "content": answer.strip()})
                    low = answer.lower()
                    assertive = any(k in low for k in ["i suggest", "i think", "could we", "propongo", "considero", "podríamos", "sugiero", "quisiera", "recomiendo"])
                    intercultural = any(k in low for k in ["understand", "respect", "perspective", "clarify", "comprendo", "entiendo", "respeto", "perspectiva", "aclarar"])
                    negotiation = any(k in low for k in ["price", "delivery", "volume", "compromise", "agreement", "precio", "entrega", "volumen", "acuerdo", "alternativa", "plazo", "pedido"])
                    s["feedback"] = [
                        "Comunicación asertiva: " + ("incluyes una propuesta o petición concreta." if assertive else "intenta formular una propuesta clara y respetuosa."),
                        "Comunicación intercultural: " + ("reconoces otra perspectiva o aclaras el mensaje." if intercultural else "puedes reconocer la perspectiva de la otra parte o pedir aclaración."),
                        "Estrategia de negociación: " + ("mencionas una condición negociable." if negotiation else "incluye una variable concreta: precio, volumen, plazo o alternativa."),
                    ]
                    s["step"] += 1
                    if s["step"] < len(s["turns"]):
                        next_prompt, next_stage = s["turns"][s["step"]]
                        s["history"].append({"role": "assistant", "content": f"Ronda completada. Siguiente etapa: {next_stage}.\n\n{next_prompt}"})
                    else:
                        s["finished"] = True
                        s["history"].append({"role": "assistant", "content": "La simulación ha terminado. Revisa la retroalimentación y completa la encuesta de validación."})
                    st.rerun()
        else:
            st.success("¡Simulación finalizada! Completaste las cuatro rondas.")
            st.markdown("**Resumen de la práctica**")
            st.write(f"Escenario: {s['scenario']}")
            st.write(f"Rondas completadas: {len(s['turns'])}")
            st.write("Este prototipo no certifica el nivel de idioma ni la competencia negociadora.")
            if st.button("Empezar otra simulación"):
                st.session_state.session = None
                st.rerun()

    with side:
        st.subheader("Guía de apoyo")
        st.markdown("**Frases útiles**")
        for phrase in info["phrases"]:
            st.code(phrase)
        st.markdown("**Recordatorio intercultural**")
        st.write("Escucha, evita asumir que la otra persona comparte tus normas de comunicación y confirma los acuerdos.")
        st.divider()
        st.subheader("Retroalimentación orientativa")
        if s["feedback"]:
            st.caption("Se basa en palabras clave; no es una evaluación profesional.")
            for tip in s["feedback"]:
                st.write("•", tip)
        else:
            st.info("Las sugerencias aparecerán después de tu primera respuesta.")
        st.divider()
        st.subheader("Validación del prototipo")
        if s["finished"]:
            with st.form("validation_form"):
                usefulness = st.slider("¿Qué tan útil te pareció para practicar?", 1, 5, 3)
                clarity = st.slider("¿Qué tan claro fue el escenario?", 1, 5, 3)
                comment = st.text_area("¿Qué cambiarías?")
                save = st.form_submit_button("Registrar opinión")
            if save:
                s["survey"] = {"Utilidad": usefulness, "Claridad": clarity, "Comentario": comment}
                st.success("Opinión registrada en esta sesión.")
                st.json(s["survey"])
                st.caption("No se guarda en una base de datos; copia la opinión si necesitas conservarla.")
        else:
            st.caption("La encuesta se habilita al terminar las cuatro rondas.")

st.divider()
st.caption("Intercultura IA · Prototipo académico demostrativo · Las respuestas son guionizadas, no generadas por un modelo de IA real.")
