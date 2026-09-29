# marimargroup.com: deploy con GitHub y Cloudflare Workers

El sitio actual ya corre en el Worker **`marimargroup`**, con `marimargroup.com` conectado.
Este repo se conecta a ese mismo Worker, así que **no hay que tocar DNS ni correos**.

## Estructura
- `public/`: el sitio. Es lo que se publica.
- `wrangler.jsonc`: la configuración. `name` tiene que ser `marimargroup`.
- No incluye `routes` a propósito: los dominios se siguen manejando desde el panel.

## Rutas (SEO)
| Antes | Ahora |
|---|---|
| `/` y las anclas `#servicios`, `#nosotros`, `#contacto` | Iguales |
| `/index-en.html` | `/en/`, con redirección 301 (`public/_redirects`) |
| `/logo-full.png`, `/logo-icon.png`, `/puerto-marimar.jpg` | Iguales |
| `/robots.txt`, `/sitemap.xml` | Iguales; el sitemap quedó corregido |

## 1. GitHub
1. Crea un repo **privado** y vacío: `marimar-web`.
2. Sube el **contenido** de esta carpeta: `wrangler.jsonc` y `public/` tienen que quedar en la raíz.
3. Crea la rama `pruebas`.

## 2. Conectar el Worker existente (sin publicar nada todavía)
Ruta: Workers & Pages → **marimargroup** → Settings → **Builds** → **Connect** → repo `marimar-web`
- Production branch: `main`
- Build command: *(vacío)*
- **Deploy command: `npx wrangler versions upload`** ← modo prueba: crea versiones, pero NO cambia marimargroup.com
- Non-production branch builds: activado, con el comando `npx wrangler versions upload`
- Root directory: `/`

En Settings → Domains & Routes, confirma que **Preview URLs** esté activado.

## 3. Probar
- Cada build genera una **Preview URL** (Deployments → Versions), del tipo `xxxx-marimargroup.jarodriguez1687.workers.dev`.
- Qué revisar: ES/EN, el menú en móvil, el formulario (abre WhatsApp), las 7 divisiones, el mapa y el clima.

## 4. Publicar (solo con la aprobación)
- Opción A: Deployments → elige la versión probada → **Deploy version** (100 %).
- Opción B: cambia el Deploy command a `npx wrangler deploy`. Desde ahí, cada push a `main` publica.
- Si algo sale mal: Deployments → versión anterior → **Rollback**.
- En Google Search Console: inspecciona `/` y vuelve a enviar `sitemap.xml`.
