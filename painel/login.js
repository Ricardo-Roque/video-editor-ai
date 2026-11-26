"use strict";
// Tela de login. Sem nenhum usuário no banco, vira "criar o primeiro acesso".
const form = document.getElementById("form");
const erro = document.getElementById("erro");
let primeiro = false;

fetch("/api/primeiro_acesso").then((r) => r.json()).then((j) => {
  if (!j.banco) { mostrarErro("Sem conexão com o banco (SUPABASE_DB_URL no .env)."); return; }
  if (j.sem_usuarios) {
    primeiro = true;
    document.getElementById("titulo").textContent = "Criar o primeiro acesso";
    document.getElementById("sub").textContent = "Ainda não há usuários. Este será o seu login; depois você cria o do sócio na aba Equipe.";
    document.getElementById("campo-nome").hidden = false;
    document.getElementById("campo-conf").hidden = false;
    form.senha.autocomplete = "new-password";
    document.getElementById("enviar").textContent = "Criar e entrar";
  }
});

function mostrarErro(t) { erro.textContent = t; erro.hidden = !t; }

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  mostrarErro("");
  const email = form.email.value.trim(), senha = form.senha.value;
  if (primeiro) {
    if (senha !== form.conf.value) return mostrarErro("As senhas não conferem.");
    const r = await fetch("/api/primeiro_acesso", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ nome: form.nome.value.trim(), email, senha }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) return mostrarErro(j.erro || "Não foi possível criar.");
  }
  const r = await fetch("/api/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, senha }) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) return mostrarErro(j.erro || "Não foi possível entrar.");
  location.href = "/";
});

// luz que segue o cursor no cartão
document.addEventListener("pointermove", (e) => {
  const r = form.getBoundingClientRect();
  form.style.setProperty("--mx", e.clientX - r.left + "px");
  form.style.setProperty("--my", e.clientY - r.top + "px");
});
