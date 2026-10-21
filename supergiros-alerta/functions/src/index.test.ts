import { strict as assert } from "node:assert";
import { test } from "node:test";

// Pure unit tests for the accepted alert type and basic field boundaries.
// Authorization and Firestore behavior require Firebase Emulator integration tests.
function isAllowedType(type: unknown): type is "TEST" {
  return type === "TEST";
}

function isValidText(title: unknown, message: unknown): boolean {
  return typeof title === "string"
    && typeof message === "string"
    && title.trim().length >= 3
    && title.trim().length <= 100
    && message.trim().length >= 3
    && message.trim().length <= 500;
}

test("MVP accepts only TEST event type", () => {
  assert.equal(isAllowedType("TEST"), true);
  assert.equal(isAllowedType("SIMULACRO"), false);
  assert.equal(isAllowedType("EMERGENCIA"), false);
  assert.equal(isAllowedType(undefined), false);
});

test("validates title and message bounds", () => {
  assert.equal(isValidText("Prueba", "No evacuar; prueba técnica."), true);
  assert.equal(isValidText("ab", "Mensaje válido"), false);
  assert.equal(isValidText("Título válido", ""), false);
  assert.equal(isValidText("x".repeat(101), "Mensaje válido"), false);
  assert.equal(isValidText("Título válido", "x".repeat(501)), false);
});
