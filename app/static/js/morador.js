// ==========================================
// COMPONENTES DE INTERFACE (UI)
// ==========================================
function showToast(message, type = "success") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "fixed bottom-6 right-6 z-50 flex flex-col gap-3";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    const bgColor = type === "success" ? "bg-green-600" : "bg-red-600";
    toast.className = `${bgColor} text-white px-6 py-3 rounded-xl shadow-xl font-semibold text-sm transform transition-all duration-300 translate-y-10 opacity-0 flex items-center gap-2`;
    toast.innerHTML = `<span class="material-symbols-outlined text-lg">${type === 'success' ? 'check_circle' : 'error'}</span> ${message}`;

    container.appendChild(toast);

    setTimeout(() => toast.classList.remove("translate-y-10", "opacity-0"), 10);
    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-y-2");
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==========================================
// LÓGICA DA APLICAÇÃO
// ==========================================
const MORADOR_ID_SIMULADO = 1;
let areasCache = {}; 
let reservasCache = {}; // Novo cache para as reservas

async function carregarAreasNoSelect() {
    try {
        const res = await fetch("/api/area/?t=" + new Date().getTime()); 
        const areas = await res.json();
        const select = document.getElementById("area");
        
        if (!select) return;
        
        select.innerHTML = '<option value="">Selecione uma área...</option>';
        
        areas.forEach(area => {
            const isAtivo = (area.ativo === true || area.ativo === 1);
            areasCache[area.id] = area;
            
            if (isAtivo) {
                select.innerHTML += `<option value="${area.id}">${area.nome} ${area.possui_taxa ? '(R$ ' + area.taxa + ')' : '(Grátis)'}</option>`;
            }
        });

        carregarMinhasReservas();
    } catch (error) {
        showToast("Erro ao carregar lista de áreas.", "error");
    }
}

async function carregarMinhasReservas() {
    try {
        const res = await fetch(`/api/reserva/morador/${MORADOR_ID_SIMULADO}`);
        const reservas = await res.json();
        const container = document.getElementById("listaReservas");
        const contador = document.getElementById("contadorReservas");

        if (!container) return;

        container.innerHTML = "";
        reservasCache = {}; // Limpa o cache a cada carregamento

        if (contador) contador.innerText = `${reservas.length} Agendadas`;

        if (reservas.length === 0) {
            container.innerHTML = `<p class="text-center text-slate-500 py-8">Você ainda não tem reservas agendadas.</p>`;
            return;
        }

        reservas.forEach(r => {
            reservasCache[r.id] = r; // Salva a reserva no cache para edição

            const areaInfo = areasCache[r.area_id];
            const nomeArea = areaInfo ? areaInfo.nome : `Área Desconhecida (ID: ${r.area_id})`;

            container.innerHTML += `
                <div class="p-6 rounded-lg border border-slate-100 hover:bg-surface-container-low transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-xl bg-primary-fixed flex items-center justify-center flex-shrink-0">
                            <span class="material-symbols-outlined text-primary">event</span>
                        </div>
                        <div>
                            <h4 class="font-bold text-on-surface">${nomeArea}</h4>
                            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-on-surface-variant mt-1">
                                <span class="flex items-center gap-1.5">
                                    <span class="material-symbols-outlined text-[18px]">calendar_month</span>
                                    ${r.data_reserva}
                                </span>
                                <span class="flex items-center gap-1.5">
                                    <span class="material-symbols-outlined text-[18px]">schedule</span>
                                    ${r.horario_inicio} - ${r.horario_fim}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <button onclick="editarReserva(${r.id})" class="text-blue-600 hover:text-blue-800 font-bold text-sm transition">Editar</button>
                        <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">${r.status}</span>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        showToast("Erro ao carregar suas reservas.", "error");
    }
}

// ==========================================
// FUNÇÕES DE EDIÇÃO
// ==========================================
function editarReserva(id) {
    const r = reservasCache[id];
    if (!r) return;

    // Preenche os campos do formulário
    const inputReservaId = document.getElementById("reserva_id");
    if(inputReservaId) inputReservaId.value = r.id;

    document.getElementById("area").value = r.area_id;
    document.getElementById("data").value = r.data_reserva;
    document.getElementById("inicio").value = r.horario_inicio.substring(0, 5); // Ex: "10:00:00" -> "10:00"
    document.getElementById("fim").value = r.horario_fim.substring(0, 5);

    // Ajusta os botões visuais
    const btnSalvar = document.getElementById("btnSalvar");
    const btnCancelar = document.getElementById("btnCancelar");

    if (btnSalvar) {
        btnSalvar.innerText = "Atualizar Reserva";
        btnSalvar.classList.replace("w-full", "w-2/3");
    }
    if (btnCancelar) {
        btnCancelar.classList.remove("hidden");
    }
    
    // Rola a tela suavemente para o topo onde está o formulário
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function cancelarEdicao() {
    const form = document.getElementById("reservaForm");
    if(form) form.reset();

    const inputReservaId = document.getElementById("reserva_id");
    if(inputReservaId) inputReservaId.value = "";

    const btnSalvar = document.getElementById("btnSalvar");
    const btnCancelar = document.getElementById("btnCancelar");

    if (btnSalvar) {
        btnSalvar.innerText = "Confirmar Reserva";
        btnSalvar.classList.replace("w-2/3", "w-full");
    }
    if (btnCancelar) {
        btnCancelar.classList.add("hidden");
    }
}

// ==========================================
// SUBMISSÃO DO FORMULÁRIO (CRIAÇÃO/EDIÇÃO)
// ==========================================
const form = document.getElementById("reservaForm");
if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const areaId = document.getElementById("area").value;
        if (!areaId) {
            showToast("Por favor, selecione uma área.", "error");
            return;
        }

        const inputReservaId = document.getElementById("reserva_id");
        const reservaId = inputReservaId ? inputReservaId.value : "";

        // O backend (FastAPI/Time) exige formato HH:MM:SS. Se o input devolver HH:MM, adicionamos os segundos
        let hor_inicio = document.getElementById("inicio").value;
        let hor_fim = document.getElementById("fim").value;
        if (hor_inicio.length === 5) hor_inicio += ":00";
        if (hor_fim.length === 5) hor_fim += ":00";

        const data = {
            area_id: parseInt(areaId),
            morador_id: MORADOR_ID_SIMULADO,
            data_reserva: document.getElementById("data").value,
            horario_inicio: hor_inicio, 
            horario_fim: hor_fim,
            status: "CONFIRMADA", 
            valor_pago: 0.0 
        };

        // Define a rota e o método HTTP dependendo se estamos criando ou editando
        const url = reservaId ? `/api/reserva/${reservaId}` : "/api/reserva/";
        const method = reservaId ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method: method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                showToast(reservaId ? "Reserva atualizada com sucesso!" : "Reserva confirmada com sucesso!", "success");
                cancelarEdicao(); // Limpa e restaura a visualização do formulário
                carregarMinhasReservas();
            } else {
                const erro = await res.json();
                showToast("Erro ao processar: " + (erro.detail || "Verifique os dados"), "error");
            }
        } catch (error) {
            showToast("Erro de comunicação com o servidor.", "error");
        }
    });
}

// Inicia a aplicação carregando os dados
carregarAreasNoSelect();