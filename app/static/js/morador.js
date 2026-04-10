const form = document.getElementById("reservaForm");

form.addEventListener("submit", (e) => {
    e.preventDefault();

    const data = {
        area: document.getElementById("area").value,
        data: document.getElementById("data").value,
        inicio: document.getElementById("inicio").value,
        fim: document.getElementById("fim").value
    };

    console.log("Reserva criada:", data);

    alert("Reserva enviada (simulação)");
});

// 🔹 INFO DA ÁREA
document.getElementById("area").addEventListener("change", () => {
    const area = document.getElementById("area").value;
    const info = document.getElementById("infoArea");

    if (area == "1") {
        info.innerText = "Área paga: R$50";
    } else {
        info.innerText = "Área gratuita";
    }
});

// 🔹 AÇÕES
function editar() {
    alert("Editar reserva (futuro)");
}

function cancelar() {
    alert("Cancelamento pode gerar multa!");
}