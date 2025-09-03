# app/services/validation_service.py
import numpy as np
import face_recognition
from sqlalchemy.orm import joinedload
from typing import List

from app.analysis.liveness_analyzer import is_blinking
from app.analysis.geometry_analyzer import get_geometry_ratios, compare_geometry
from app.models._manager import db
from app.models.bitacora import Bitacora
from app.models.usuario import Usuario
from .capture_process import capturar_y_procesar, DatosMuestra

MIN_PARPADEOS = 1
MIN_COINCIDENCIAS = 8
TOLERANCIA_DISTANCIA = 0.5


def _encontrar_mejor_coincidencia(
    muestras_capturadas: List[DatosMuestra], usuarios: List[Usuario]
) -> tuple[int | None, int]:
    embeddings_capturados = [m["embedding"] for m in muestras_capturadas]
    conteo = {user.id: 0 for user in usuarios}

    for user in usuarios:
        if not user.muestras:
            continue
        embeddings_conocidos = np.array([m.embedding for m in user.muestras])
        for emb in embeddings_capturados:
            distancias = face_recognition.face_distance(embeddings_conocidos, emb)
            if np.any(distancias < TOLERANCIA_DISTANCIA):
                conteo[user.id] += 1

    if not any(conteo.values()):
        return None, 0

    # CORRECCIÓN 1: Usar lambda para que Pylance entienda la función key.
    mejor_user_id = max(conteo, key=lambda k: conteo[k])
    return mejor_user_id, conteo[mejor_user_id]


async def validar_usuario() -> bool:
    log = Bitacora()
    usuarios_conocidos = db.query(Usuario).options(joinedload(Usuario.muestras)).all()
    if not usuarios_conocidos:
        print("No hay usuarios registrados.")
        return False

    muestras_capturadas = await capturar_y_procesar(duration_seconds=4)
    if not muestras_capturadas:
        print("❌ No se detectó ninguna cara.")
        return False

    parpadeos = sum(1 for m in muestras_capturadas if is_blinking(m["landmarks"]))
    log.pr_liveness = parpadeos >= MIN_PARPADEOS
    if not log.pr_liveness:
        print(f"❌ Denegado: Prueba de vida fallida ({parpadeos}/{MIN_PARPADEOS}).")
        log.save()
        return False

    mejor_user_id, num_coincidencias = _encontrar_mejor_coincidencia(
        muestras_capturadas, usuarios_conocidos
    )

    log.user_id = mejor_user_id
    log.pr_descriptor = num_coincidencias >= MIN_COINCIDENCIAS
    if not log.pr_descriptor:
        print(
            f"❌ Denegado: Identidad no reconocida ({num_coincidencias}/{MIN_COINCIDENCIAS})."
        )
        log.save()
        return False

    candidato = next(u for u in usuarios_conocidos if u.id == mejor_user_id)
    print(f"ℹ️ Candidato: {candidato.nombre}. Verificando geometría...")

    landmarks_conocidos = [m.landmarks for m in candidato.muestras]
    ratios_capturados = get_geometry_ratios(muestras_capturadas[0]["landmarks"])

    # CORRECCIÓN 2: Convertir el resultado de NumPy a un booleano nativo de Python.
    resultado_geometria = compare_geometry(ratios_capturados, landmarks_conocidos)
    log.pr_geometry = bool(resultado_geometria)

    if not log.pr_geometry:
        print("❌ Denegado: Geometría facial inconsistente.")
        log.save()
        return False

    print(f"✅ Acceso concedido a: {candidato.nombre}")
    print(f"(Parpadeos: {parpadeos}, Coincidencias: {num_coincidencias})")
    log.status = True
    log.save()
    return True
