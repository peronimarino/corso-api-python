const API_URL =
    "https://ominous-disco-gxqv9jg7xgxp3p4jq-8000.app.github.dev";

async function effettuaLogin() {

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Compila tutti i campi");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        const dati = await response.json();

        if (!response.ok) {
            alert(dati.detail || "Credenziali non valide");
            return;
        }

        localStorage.setItem(
            "session_token",
            dati.token
        );

        localStorage.setItem(
            "username",
            username
        );


        window.location.href = "catalogo.html";

    }
    catch (error) {

        console.error(error);

        alert(
            "Errore di connessione al server"
        );
    }
}