import pycountry

countries = [country.name for country in pycountry.countries]
areas = [
    "Tecnología de la Información (TI)",
    "Ingeniería",
    "Salud",
    "Finanzas",
    "Educación",
    "Gestión Empresarial",
    "Marketing y Ventas",
    "Recursos Humanos (RRHH)",
    "Creatividad y Diseño",
    "Ciencia e Investigación",
    "Legal",
    "Construcción y Oficios",
    "Hostelería y Turismo",
    "Manufactura",
    "Agricultura",
    "Transporte y Logística",
    "Atención al Cliente",
    "Medios de Comunicación",
    "Servicios Sociales y Sin Fines de Lucro",
    "Gobierno y Administración Pública"
]

carreras = {
    "Ingenierías": [
        "Ingeniería Informática",
        "Ingeniería Industrial",
        "Ingeniería de Telecomunicaciones",
        "Ingeniería Civil",
        "Ingeniería Química",
        "Ingeniería Mecánica",
        "Ingeniería Eléctrica",
        "Ingeniería Aeroespacial",
        "Ingeniería Biomédica"
    ],
    "Ciencias de la Salud": [
        "Medicina",
        "Enfermería",
        "Psicología",
        "Farmacia",
        "Odontología",
        "Fisioterapia",
        "Veterinaria",
        "Biología",
        "Biotecnología"
    ],
    "Ciencias Sociales y Jurídicas": [
        "Derecho",
        "Administración y Dirección de Empresas (ADE)",
        "Economía",
        "Periodismo",
        "Comunicación Audiovisual",
        "Ciencias Políticas",
        "Sociología",
        "Relaciones Internacionales",
        "Marketing"
    ],
    "Artes y Humanidades": [
        "Filología (Inglesa, Hispánica, etc.)",
        "Historia",
        "Filosofía",
        "Bellas Artes",
        "Diseño",
        "Traducción e Interpretación",
        "Musicología",
        "Historia del Arte",
        "Pedagogía"
    ],
    "Ciencias": [
        "Matemáticas",
        "Física",
        "Química",
        "Estadística",
        "Geología",
        "Ciencias Ambientales",
        "Bioquímica",
        "Biotecnología",
        "Óptica y Optometría"
    ]
}

motivaciones = ["Salto de carrera", "Cambio de carrera", "Desarrollo personal", "Aplicación en negocio propio"]