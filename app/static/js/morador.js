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
let reservasCache = {};

// ==========================================
// FUNÇÃO DE CONFLITO (FORA DO SUBMIT)
// ==========================================
function temConflito(novaInicio, novaFim, data, areaId, reservaEditandoId = null) {
    return Object.values(reservasCache).some(r => {
        if (r.data_reserva !== data) return false;
        if (r.area_id != areaId) return false;

        if (reservaEditandoId && r.id == reservaEditandoId) return false;

        const inicioExistente = r.horario_inicio.substring(0,5);
        const fimExistente = r.horario_fim.substring(0,5);

        return (
            novaInicio < fimExistente &&
            novaFim > inicioExistente
        );
    });
}

// ==========================================
// CARREGAMENTO
// ==========================================
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
                select.innerHTML += `<option value="${area.id}">${area.nome}</option>`;
            }
        });

        carregarMinhasReservas();
    } catch (error) {
        showToast("Erro ao carregar áreas.", "error");
    }
}

async function carregarMinhasReservas() {
    try {
        const res = await fetch(`/api/reserva/morador/${MORADOR_ID_SIMULADO}`);
        const reservas = await res.json();
        const container = document.getElementById("listaReservas");

        if (!container) return;

        container.innerHTML = "";
        reservasCache = {};

        reservas.forEach(r => {
            reservasCache[r.id] = r;

            container.innerHTML += `
                <div>
                    ${r.data_reserva} - ${r.horario_inicio} até ${r.horario_fim}
                </div>
            `;
        });

    } catch (error) {
        showToast("Erro ao carregar reservas.", "error");
    }
}

// ==========================================
// SUBMIT (COM TODAS AS VALIDAÇÕES)
// ==========================================
const form = document.getElementById("reservaForm");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const areaId = document.getElementById("area").value;
        const dataReserva = document.getElementById("data").value;
        const inicio = document.getElementById("inicio").value;
        const fim = document.getElementById("fim").value;

        const inputReservaId = document.getElementById("reserva_id");
        const reservaId = inputReservaId ? inputReservaId.value : "";

        // =============================
        // VALIDAÇÕES
        // =============================
        if (!areaId) {
            showToast("Selecione uma área.", "error");
            return;
        }

        if (!dataReserva) {
            showToast("Informe a data.", "error");
            return;
        }

        if (!inicio || !fim) {
            showToast("Preencha os horários.", "error");
            return;
        }

        if (inicio === fim) {
            showToast("Horários não podem ser iguais.", "error");
            return;
        }

        if (inicio > fim) {
            showToast("Início deve ser menor que o fim.", "error");
            return;
        }

        if (temConflito(inicio, fim, dataReserva, areaId, reservaId)) {
            showToast("Já existe reserva nesse horário.", "error");
            return;
        }

        // =============================
        // FORMATAÇÃO
        // =============================
        let hor_inicio = inicio.length === 5 ? inicio + ":00" : inicio;
        let hor_fim = fim.length === 5 ? fim + ":00" : fim;

        const data = {
            area_id: parseInt(areaId),
            morador_id: MORADOR_ID_SIMULADO,
            data_reserva: dataReserva,
            horario_inicio: hor_inicio,
            horario_fim: hor_fim,
            status: "CONFIRMADA",
            valor_pago: 0.0
        };

        const url = reservaId ? `/api/reserva/${reservaId}` : "/api/reserva/";
        const method = reservaId ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method: method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                showToast("Reserva salva com sucesso!", "success");
                form.reset();
                carregarMinhasReservas();
            } else {
                const erro = await res.json();
                showToast(erro.detail || "Erro ao salvar.", "error");
            }
        } catch {
            showToast("Erro de conexão.", "error");
        }
    });
}

// ==========================================
// INIT
// ==========================================
carregarAreasNoSelect();