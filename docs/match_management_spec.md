# Especificación Funcional: Gestión de Partidos (Edición y Eliminación)

**Objetivo:** Permitir que el administrador corrija la fecha y hora de los partidos o elimine aquellos que fueron creados por error, asegurando la integridad de los datos de predicciones.

**Actor:** Administrador.

**Precondiciones:** 
- El usuario debe estar autenticado con rol de Administrador.
- El partido a modificar/eliminar debe existir en la base de datos.

**Flujo Principal - Edición de Fecha:**
1. El administrador accede al **[Panel de Gestión de Partidos]**.
2. El administrador selecciona el partido cuya fecha desea modificar.
3. El sistema presenta un **[Selector de Fecha y Hora]** con el valor actual.
4. El administrador modifica la fecha/hora y confirma la acción.
5. El sistema valida el formato y actualiza el registro.
6. El sistema muestra un mensaje de **[Confirmación de Actualización]**.

**Flujo Principal - Eliminación de Partido:**
1. El administrador selecciona la opción de **[Eliminar Partido]**.
2. El sistema verifica si existen predicciones asociadas a dicho partido.
3. **Si no hay predicciones**: El sistema elimina el partido y muestra un mensaje de **[Confirmación de Eliminación]**.
4. **Si hay predicciones**: El sistema bloquea la acción y muestra un mensaje de **[Error/Advertencia]** indicando que el partido no puede eliminarse porque ya cuenta con predicciones.

**Criterios de Aceptación:**
- Solo administradores pueden editar o eliminar partidos.
- La edición de fecha solo está permitida para partidos en estado `pending` o `in_progress`.
- La eliminación es imposible si existe al menos una predicción realizada por cualquier usuario.
- Los cambios se reflejan inmediatamente en todas las vistas del sistema.

---

### Asunciones (No Técnicas/Funcionales)

1. Existe un panel o vista de administración dedicada donde se listan los partidos.
2. La "fecha" incluye tanto el día como la hora exacta del encuentro.
3. Solo se pueden editar los partidos en estado `pending` o `in_progress`.
4. La edición es instantánea y no requiere de un proceso de aprobación de otro administrador.
5. El cambio de fecha no dispara notificaciones automáticas a los usuarios finales.
6. No existen restricciones de negocio sobre la nueva fecha (ej. no se puede mover un partido a una fecha anterior al inicio del torneo).
7. La eliminación del partido es permanente y no existe una "papelera de reciclaje".
8. El sistema informará explícitamente al administrador la razón por la cual un partido no puede ser eliminado (ej: "Existen predicciones asociadas").
