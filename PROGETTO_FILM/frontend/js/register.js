const API_URL =
    "https://ominous-disco-gxqv9jg7xgxp3p4jq-8000.app.github.dev";

async function effettuaRegistrazione()
{
    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value.trim();

    if(!username || !password)
    {
        alert("Compila tutti i campi");
        return;
    }

    try
    {
        const response = await fetch(
            `${API_URL}/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const dati =
            await response.json();

        if(!response.ok)
        {
            alert(
                dati.detail ||
                "Errore durante la registrazione"
            );

            return;
        }

        alert(
            "Registrazione completata con successo!"
        );

        window.location.href =
            "login.html";
    }

    catch(error)
    {
        console.error(error);

        alert(
            "Errore di connessione col server"
        );
    }
}
