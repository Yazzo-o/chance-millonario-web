import { initializeApp } from "firebase-admin/app";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { onCall, HttpsError } from "firebase-functions/v2/https";

initializeApp();
const db = getFirestore();

type TestAlertInput = {
  type?: string;
  title?: string;
  message?: string;
  siteId?: string;
};

export const createTestAlert = onCall(
  { region: "southamerica-east1", enforceAppCheck: true },
  async (request) => {
    if (!request.auth) {
      throw new HttpsError("unauthenticated", "Debes iniciar sesión.");
    }

    const userSnapshot = await db.collection("users").doc(request.auth.uid).get();
    const role = userSnapshot.get("role");
    if (!["sst_admin", "system_admin"].includes(role)) {
      throw new HttpsError("permission-denied", "No tienes permiso para crear pruebas.");
    }

    const input = (request.data ?? {}) as TestAlertInput;

    // Guardrail: this initial implementation is TEST-only.
    if (input.type !== "TEST") {
      throw new HttpsError(
        "failed-precondition",
        "Este MVP solo admite alertas de prueba (TEST)."
      );
    }

    const title = String(input.title ?? "Prueba de SuperGIROS Alerta").trim();
    const message = String(input.message ?? "Esta es una prueba técnica. No evacuar.").trim();

    if (title.length < 3 || title.length > 100 || message.length < 3 || message.length > 500) {
      throw new HttpsError("invalid-argument", "Título o mensaje fuera de los límites permitidos.");
    }

    const alertRef = db.collection("alerts").doc();
    await alertRef.set({
      id: alertRef.id,
      type: "TEST",
      status: "CREATED",
      title,
      message,
      siteId: input.siteId ? String(input.siteId).slice(0, 80) : null,
      createdBy: request.auth.uid,
      createdAt: FieldValue.serverTimestamp(),
      delivery: {
        push: "NOT_CONFIGURED",
        whatsapp: "NOT_CONFIGURED",
        voice: "NOT_CONFIGURED"
      }
    });

    return {
      alertId: alertRef.id,
      status: "CREATED",
      note: "Registrada como prueba. No se envió ninguna notificación ni llamada."
    };
  }
);
