/**
 * ATP v0.8.0+ - Google Authentication Provider
 * ============================================
 * Implementación de autenticación con Google Identity Services
 */

interface GoogleUser {
    email: string;
    name: string;
    picture: string;
    sub: string;
}

export class GoogleAuthService {
    private static clientId: string = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";

    /**
     * Inicializa el cliente de Google en el DOM
     */
    static init(callback: (response: any) => void) {
        if (typeof window === "undefined") return;

        const script = document.createElement("script");
        script.src = "https://accounts.google.com/gsi/client";
        script.async = true;
        script.defer = true;
        script.onload = () => {
            // @ts-ignore
            window.google.accounts.id.initialize({
                client_id: this.clientId,
                callback: callback,
            });
        };
        document.head.appendChild(script);
    }

    /**
     * Muestra el botón de "One Tap" o el botón personalizado
     */
    static renderButton(elementId: string) {
        // @ts-ignore
        if (window.google) {
            // @ts-ignore
            window.google.accounts.id.renderButton(
                document.getElementById(elementId),
                { theme: "outline", size: "large", width: "100%" }
            );
        }
    }

    /**
     * Decodifica el token JWT de Google (Credencial)
     */
    static decodeCredential(credential: string): GoogleUser {
        const base64Url = credential.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
            atob(base64)
                .split("")
                .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
                .join("")
        );
        return JSON.parse(jsonPayload);
    }
}

export default GoogleAuthService;
