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

function customConfirm(message) {
    return new Promise((resolve) => {
        const overlay = document.createElement("div");
        overlay.className = "fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center opacity-0 transition-opacity duration-300";
        
        const modal = document.createElement("div");
        modal.className = "bg-white p-6 rounded-2xl shadow-2xl max-w-sm w-full mx-4 transform scale-95 transition-transform duration-300";
        modal.innerHTML = `
            <div class="flex items-center gap-3 mb-3 text-blue-700">
                <span class="material-symbols-outlined text-2xl">help</span>
                <h3 class="text-lg font-bold">Confirmação</h3>
            </div>
            <p class="text-slate-600 mb-6 font-medium">${message}</p>
            <div class="flex justify-end gap-3">
                <button id="btnCancel" class="px-5 py-2.5 bg-slate-100 text-slate-700 rounded-xl font-bold hover:bg-slate-200 transition">Cancelar</button>
                <button id="btnConfirm" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition shadow-md">Sim, alterar</button>
            </div>
        `;
        
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        setTimeout(() => {
            overlay.classList.remove("opacity-0");
            modal.classList.remove("scale-95");
        }, 10);

        const close = (result) => {
            overlay.classList.add("opacity-0");
            modal.classList.add("scale-95");
            setTimeout(() => {
                overlay.remove();
                resolve(result);
            }, 300);
        };

        modal.querySelector("#btnCancel").onclick = () => close(false);
        modal.querySelector("#btnConfirm").onclick = () => close(true);
    });
}

// ==========================================
// LÓGICA DA APLICAÇÃO
// ==========================================
let areasCache = {};

async function carregarAreas() {
    const res = await fetch("/api/area/?t=" + new Date().getTime());
    const areas = await res.json();
    const lista = document.getElementById("listaAreas");
    lista.innerHTML = "";
    areasCache = {};

    areas.forEach(area => {
        areasCache[area.id] = area;
        
        const isAtivo = (area.ativo === true || area.ativo === 1);
            
        const statusBadge = isAtivo 
            ? `<span class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold">Ativa</span>`
            : `<span class="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-bold">Inativa</span>`;
            
        const actionBtn = isAtivo
            ? `<button onclick="alternarStatus(${area.id})" class="text-red-500 hover:text-red-700 font-medium text-sm transition">Desativar</button>`
            : `<button onclick="alternarStatus(${area.id})" class="text-green-600 hover:text-green-800 font-medium text-sm transition">Ativar</button>`;

        lista.innerHTML += `
            <tr class="border-b ${!isAtivo ? 'opacity-60 bg-slate-50' : ''}">
                <td class="py-4 font-semibold text-slate-800">${area.nome} ${statusBadge}</td>
                <td class="py-4 text-slate-600">${area.possui_taxa ? 'R$ ' + area.taxa : 'Grátis'}</td>
                <td class="py-4 text-slate-600">S: ${area.limite_semanal} / M: ${area.limite_mensal}</td>
                <td class="py-4 text-right space-x-4">
                    <button onclick="preencherFormulario(${area.id})" class="text-blue-600 hover:text-blue-800 font-medium text-sm transition">Editar</button>
                    ${actionBtn}
                </td>
            </tr>
        `;
    });
}

function preencherFormulario(id) {
    const area = areasCache[id];
    if(!area) return;

    document.getElementById("area_id").value = area.id;
    document.getElementById("nome").value = area.nome;
    document.getElementById("descricao").value = area.descricao || "";
    document.getElementById("possui_taxa").checked = area.possui_taxa;
    document.getElementById("taxa").value = area.taxa;
    document.getElementById("limite_semanal").value = area.limite_semanal;
    document.getElementById("limite_mensal").value = area.limite_mensal;

    document.getElementById("btnSalvar").innerText = "Atualizar Área";
    document.getElementById("btnSalvar").classList.replace("w-full", "w-2/3");
    document.getElementById("btnCancelar").classList.remove("hidden");
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function cancelarEdicao() {
    document.getElementById("formArea").reset();
    document.getElementById("area_id").value = "";
    document.getElementById("btnSalvar").innerText = "Salvar Área";
    document.getElementById("btnSalvar").classList.replace("w-2/3", "w-full");
    document.getElementById("btnCancelar").classList.add("hidden");
}

document.getElementById("formArea").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("area_id").value;
    const data = {
        nome: document.getElementById("nome").value,
        descricao: document.getElementById("descricao").value,
        possui_taxa: document.getElementById("possui_taxa").checked,
        taxa: parseFloat(document.getElementById("taxa").value) || 0,
        limite_semanal: parseInt(document.getElementById("limite_semanal").value) || 0,
        limite_mensal: parseInt(document.getElementById("limite_mensal").value) || 0,
        ativo: true
    };

    const url = id ? `/api/area/${id}` : "/api/area/";
    const method = id ? "PUT" : "POST";

    const res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        showToast(id ? "Área atualizada com sucesso!" : "Área criada com sucesso!", "success");
        cancelarEdicao();
        carregarAreas();
    } else {
        showToast("Erro ao processar a requisição.", "error");
    }
});

async function alternarStatus(id) {
    // Usando o nosso novo Confirm Bonito em vez do nativo
    if (await customConfirm("Tem a certeza que deseja alterar o status desta área?")) {
        try {
            const res = await fetch(`/api/area/${id}/status`, { method: "PATCH" });
            if (res.ok) {
                showToast("Status alterado com sucesso!", "success");
                carregarAreas();
            } else {
                showToast("Erro ao alterar status.", "error");
            }
        } catch (error) {
            showToast("Erro de conexão.", "error");
        }
    }
}

carregarAreas();