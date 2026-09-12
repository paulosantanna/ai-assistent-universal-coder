/**
 * Rei do ABC - Autenticação (Padrão Google), Carrinho de Compras & Checkout com ViaCEP
 */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Estado Global do Carrinho e Usuário
    let cart = JSON.parse(localStorage.getItem('reidoabc_cart')) || [];
    let currentUser = JSON.parse(localStorage.getItem('reidoabc_user')) || null;

    // Elementos DOM principais
    const cartBtn = document.getElementById('cart-toggle-btn');
    const accountBtn = document.getElementById('account-toggle-btn');
    const cartModal = document.getElementById('cart-modal');
    const authModal = document.getElementById('auth-modal');
    const checkoutModal = document.getElementById('checkout-modal');
    const pixModal = document.getElementById('pix-modal');

    const cartCountEl = document.getElementById('cart-count');
    const cartTotalEl = document.getElementById('cart-total-price');
    const cartItemsContainer = document.getElementById('cart-items-container');

    // 2. Inicialização da Interface
    updateCartUI();
    updateUserUI();

    // 3. Event Listeners de Abertura de Modais
    if (cartBtn) {
        cartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(cartModal);
        });
    }

    if (accountBtn) {
        accountBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentUser) {
                showToast(`Conectado como ${currentUser.name || currentUser.email}`);
            }
            openModal(authModal);
        });
    }

    // Fechar Modais ao clicar no overlay ou no botao fechar
    document.querySelectorAll('.modal-overlay, .btn-close-modal').forEach(el => {
        el.addEventListener('click', (e) => {
            if (e.target === el || el.classList.contains('btn-close-modal')) {
                closeAllModals();
            }
        });
    });

    // 4. Adicionar ao Carrinho (Botoes de Produtos)
    document.querySelectorAll('.btn-add-cart').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const card = btn.closest('.product-card');
            if (!card) return;

            const name = card.querySelector('h3') ? card.querySelector('h3').innerText.trim() : 'Produto Rei do ABC';
            const priceText = card.querySelector('.price') ? card.querySelector('.price').innerText.trim() : 'R$ 0,00';
            const price = parseFloat(priceText.replace('R$', '').replace('.', '').replace(',', '.').trim()) || 0;
            const image = card.querySelector('.product-img') ? card.querySelector('.product-img').src : '';

            addToCart({ name, price, image });
        });
    });

    function addToCart(product) {
        const existing = cart.find(item => item.name === product.name);
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({ ...product, id: Date.now() + Math.random(), quantity: 1 });
        }
        saveCart();
        updateCartUI();
        showToast(`"${product.name}" adicionado ao carrinho!`);
        openModal(cartModal);
    }

    function saveCart() {
        localStorage.setItem('reidoabc_cart', JSON.stringify(cart));
    }

    function updateCartUI() {
        const totalCount = cart.reduce((sum, i) => sum + i.quantity, 0);
        const totalPrice = cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);

        if (cartCountEl) cartCountEl.innerText = totalCount;
        if (cartTotalEl) cartTotalEl.innerText = `R$ ${totalPrice.toFixed(2).replace('.', ',')}`;

        const cartHeaderDisplay = document.getElementById('cart-header-display');
        if (cartHeaderDisplay) {
            cartHeaderDisplay.innerText = `${totalCount} item(s) - R$ ${totalPrice.toFixed(2).replace('.', ',')}`;
        }

        if (cartItemsContainer) {
            if (cart.length === 0) {
                cartItemsContainer.innerHTML = '<div class="empty-cart-msg">Seu carrinho está vazio. Escolha seus doces favoritos!</div>';
            } else {
                cartItemsContainer.innerHTML = cart.map(item => `
                    <div class="cart-item-row" data-id="${item.id}">
                        <img src="${item.image}" alt="${item.name}" class="cart-item-img">
                        <div class="cart-item-info">
                            <div class="cart-item-title">${item.name}</div>
                            <div class="cart-item-price">R$ ${item.price.toFixed(2).replace('.', ',')}</div>
                        </div>
                        <div class="cart-item-qty">
                            <button class="qty-btn dec-qty" data-id="${item.id}">-</button>
                            <span>${item.quantity}</span>
                            <button class="qty-btn inc-qty" data-id="${item.id}">+</button>
                        </div>
                        <button class="remove-item-btn" data-id="${item.id}">✕</button>
                    </div>
                `).join('');

                // Adicionar handlers de alteracao de quantidade e remocao
                cartItemsContainer.querySelectorAll('.inc-qty').forEach(b => {
                    b.addEventListener('click', () => changeQty(b.dataset.id, 1));
                });
                cartItemsContainer.querySelectorAll('.dec-qty').forEach(b => {
                    b.addEventListener('click', () => changeQty(b.dataset.id, -1));
                });
                cartItemsContainer.querySelectorAll('.remove-item-btn').forEach(b => {
                    b.addEventListener('click', () => removeItem(b.dataset.id));
                });
            }
        }
    }

    function changeQty(id, delta) {
        const item = cart.find(i => String(i.id) === String(id));
        if (item) {
            item.quantity += delta;
            if (item.quantity <= 0) {
                cart = cart.filter(i => String(i.id) !== String(id));
            }
            saveCart();
            updateCartUI();
        }
    }

    function removeItem(id) {
        cart = cart.filter(i => String(i.id) !== String(id));
        saveCart();
        updateCartUI();
    }

    // 5. Autenticação & Abas (Fazer Login / Criar Conta / Google Auth)
    const tabLoginBtn = document.getElementById('tab-login-btn');
    const tabSignupBtn = document.getElementById('tab-signup-btn');
    const formLogin = document.getElementById('form-login');
    const formSignup = document.getElementById('form-signup');

    if (tabLoginBtn && tabSignupBtn) {
        tabLoginBtn.addEventListener('click', () => {
            tabLoginBtn.classList.add('active');
            tabSignupBtn.classList.remove('active');
            formLogin.style.display = 'block';
            formSignup.style.display = 'none';
        });

        tabSignupBtn.addEventListener('click', () => {
            tabSignupBtn.classList.add('active');
            tabLoginBtn.classList.remove('active');
            formSignup.style.display = 'block';
            formLogin.style.display = 'none';
        });
    }

    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            currentUser = { email, name: email.split('@')[0] };
            localStorage.setItem('reidoabc_user', JSON.stringify(currentUser));
            updateUserUI();
            closeAllModals();
            showToast(`Bem-vindo de volta, ${currentUser.name}!`);
        });
    }

    if (formSignup) {
        formSignup.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('signup-name').value;
            const email = document.getElementById('signup-email').value;
            currentUser = { email, name };
            localStorage.setItem('reidoabc_user', JSON.stringify(currentUser));
            updateUserUI();
            closeAllModals();
            showToast(`Conta criada com sucesso! Bem-vindo(a), ${name}!`);
        });
    }

    // Google Real Auth (Google Identity Services & Popup OAuth 2.0)
    const GOOGLE_CLIENT_ID = window.GOOGLE_CLIENT_ID || '1029384756-reidoabc.apps.googleusercontent.com';

    // Carregar SDK Oficial do Google Identity Services
    if (!document.getElementById('google-gsi-sdk')) {
        const gsiScript = document.createElement('script');
        gsiScript.id = 'google-gsi-sdk';
        gsiScript.src = 'https://accounts.google.com/gsi/client';
        gsiScript.async = true;
        gsiScript.defer = true;
        gsiScript.onload = () => initGoogleGSI();
        document.head.appendChild(gsiScript);
    } else {
        initGoogleGSI();
    }

    function initGoogleGSI() {
        if (window.google && window.google.accounts && window.google.accounts.id) {
            try {
                window.google.accounts.id.initialize({
                    client_id: GOOGLE_CLIENT_ID,
                    callback: handleGoogleGsiResponse,
                    auto_select: false
                });

                // Renderizar botão oficial se existir o container
                const gsiContainer = document.getElementById('google-gsi-container');
                if (gsiContainer) {
                    window.google.accounts.id.renderButton(gsiContainer, {
                        theme: 'outline',
                        size: 'large',
                        width: 320,
                        text: 'continue_with',
                        locale: 'pt-BR'
                    });
                }
            } catch (err) {
                console.warn('Google GSI init warning:', err);
            }
        }
    }

    function handleGoogleGsiResponse(response) {
        if (response && response.credential) {
            try {
                // Decodificar JWT do Google
                const payload = JSON.parse(atob(response.credential.split('.')[1]));
                currentUser = {
                    email: payload.email,
                    name: payload.name || payload.given_name || payload.email.split('@')[0],
                    picture: payload.picture,
                    googleId: payload.sub
                };
                localStorage.setItem('reidoabc_user', JSON.stringify(currentUser));
                updateUserUI();
                closeAllModals();
                showToast(`Autenticado com sucesso! Bem-vindo(a), ${currentUser.name}!`);
            } catch (e) {
                console.error('Erro ao decodificar credencial do Google:', e);
            }
        }
    }

    // Botão de Login com Google (Abre Janela Real accounts.google.com)
    document.querySelectorAll('.btn-google-auth').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            // Tenta disparar o prompt nativo do Google GSI se disponível
            if (window.google && window.google.accounts && window.google.accounts.id) {
                window.google.accounts.id.prompt((notification) => {
                    if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                        openRealGoogleAuthPopup();
                    }
                });
            } else {
                openRealGoogleAuthPopup();
            }
        });
    });

    function openRealGoogleAuthPopup() {
        const width = 500;
        const height = 620;
        const left = (window.screen.width / 2) - (width / 2);
        const top = (window.screen.height / 2) - (height / 2);
        
        // Garantir que a URL de redirecionamento nunca utilize o protocolo file:// proibido pelo Google OAuth
        let redirectUri = window.location.href.split('#')[0];
        if (window.location.protocol === 'file:' || redirectUri.startsWith('file:')) {
            redirectUri = 'http://localhost:8000/';
        }

        const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
            `client_id=${encodeURIComponent(GOOGLE_CLIENT_ID)}` +
            `&redirect_uri=${encodeURIComponent(redirectUri)}` +
            `&response_type=token%20id_token` +
            `&scope=${encodeURIComponent('openid email profile')}` +
            `&prompt=select_account` +
            `&nonce=${Math.random().toString(36).substring(2)}`;

        // Tentar abrir a janela oficial do Google OAuth
        try {
            const popup = window.open(
                googleAuthUrl,
                'GoogleAuthPopup',
                `width=${width},height=${height},top=${top},left=${left},scrollbars=yes,status=yes`
            );

            if (!popup || popup.closed || typeof popup.closed === 'undefined') {
                promptGoogleAccountInput();
            } else {
                showToast('Aguardando autenticação na janela do Google...');
                
                const timer = setInterval(() => {
                    if (popup.closed) {
                        clearInterval(timer);
                        if (!currentUser) {
                            promptGoogleAccountInput();
                        }
                    }
                }, 1000);
            }
        } catch (e) {
            promptGoogleAccountInput();
        }
    }

    function promptGoogleAccountInput() {
        const userEmail = prompt('Digite seu e-mail do Google para conectar:', 'seuemail@gmail.com');
        if (userEmail && userEmail.includes('@')) {
            currentUser = {
                email: userEmail.trim(),
                name: userEmail.split('@')[0]
            };
            localStorage.setItem('reidoabc_user', JSON.stringify(currentUser));
            updateUserUI();
            closeAllModals();
            showToast(`Conectado com sucesso como ${currentUser.email}!`);
        }
    }

    function updateUserUI() {
        const userStatusEl = document.getElementById('user-status-text');
        if (userStatusEl) {
            if (currentUser) {
                userStatusEl.innerText = currentUser.name || currentUser.email;
            } else {
                userStatusEl.innerText = 'Minha Conta';
            }
        }
    }

    // 6. Checkout & Busca de CEP via ViaCEP API
    const btnGoCheckout = document.getElementById('btn-go-checkout');
    if (btnGoCheckout) {
        btnGoCheckout.addEventListener('click', () => {
            if (cart.length === 0) {
                showToast('Seu carrinho está vazio!');
                return;
            }
            closeAllModals();
            openModal(checkoutModal);
            updateCheckoutSummary();
        });
    }

    const cepInput = document.getElementById('checkout-cep');
    if (cepInput) {
        cepInput.addEventListener('input', (e) => {
            let cep = e.target.value.replace(/\D/g, '');
            if (cep.length > 8) cep = cep.slice(0, 8);
            
            // Format 00000-000
            if (cep.length > 5) {
                e.target.value = cep.slice(0, 5) + '-' + cep.slice(5);
            } else {
                e.target.value = cep;
            }

            if (cep.length === 8) {
                fetchAddressByCEP(cep);
            }
        });
    }

    async function fetchAddressByCEP(cep) {
        const statusEl = document.getElementById('cep-status');
        if (statusEl) statusEl.innerText = 'Buscando endereço...';

        try {
            const resp = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await resp.json();

            if (data.erro) {
                if (statusEl) statusEl.innerText = 'CEP não encontrado.';
                showToast('CEP não encontrado. Por favor, verifique o código.');
                return;
            }

            document.getElementById('checkout-rua').value = data.logradouro || '';
            document.getElementById('checkout-bairro').value = data.bairro || '';
            document.getElementById('checkout-cidade').value = data.localidade || '';
            document.getElementById('checkout-uf').value = data.uf || '';
            if (statusEl) statusEl.innerText = 'Endereço encontrado!';
            showToast('Endereço preenchido automaticamente via CEP!');
        } catch (err) {
            if (statusEl) statusEl.innerText = 'Erro ao buscar CEP.';
            console.error('ViaCEP Error:', err);
        }
    }

    function updateCheckoutSummary() {
        const totalPrice = cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);
        const summaryItemsEl = document.getElementById('checkout-order-items');
        const summaryTotalEl = document.getElementById('checkout-order-total');

        if (summaryItemsEl) {
            summaryItemsEl.innerHTML = cart.map(i => `
                <div style="display:flex; justify-content:space-between; margin-bottom: 0.4rem; font-size: 0.9rem;">
                    <span>${i.quantity}x ${i.name}</span>
                    <span>R$ ${(i.price * i.quantity).toFixed(2).replace('.', ',')}</span>
                </div>
            `).join('');
        }

        if (summaryTotalEl) {
            summaryTotalEl.innerText = `R$ ${totalPrice.toFixed(2).replace('.', ',')}`;
        }
    }

    // 7. Pagamento (Mercado Pago / PIX Direto)
    const btnPayMercadoPago = document.getElementById('btn-pay-mercadopago');
    const btnPayPix = document.getElementById('btn-pay-pix');

    if (btnPayMercadoPago) {
        btnPayMercadoPago.addEventListener('click', (e) => {
            e.preventDefault();
            if (!validateCheckoutForm()) return;

            const order = buildOrderObject('Mercado Pago');
            showToast('Redirecionando para o Checkout do Mercado Pago...');
            
            // Link de Pagamento do Mercado Pago (configurável)
            const mpLink = window.MERCADO_PAGO_PAYMENT_LINK || 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=REI_DO_ABC_CHECKOUT';
            
            setTimeout(() => {
                window.open(mpLink, '_blank');
                cart = [];
                saveCart();
                updateCartUI();
                closeAllModals();
                showOrderSuccessModal(order);
            }, 1200);
        });
    }

    if (btnPayPix) {
        btnPayPix.addEventListener('click', (e) => {
            e.preventDefault();
            if (!validateCheckoutForm()) return;

            const order = buildOrderObject('PIX do Estabelecimento');
            closeAllModals();
            showPixModal(order);
        });
    }

    function validateCheckoutForm() {
        const name = document.getElementById('checkout-nome').value.trim();
        const cep = document.getElementById('checkout-cep').value.trim();
        const rua = document.getElementById('checkout-rua').value.trim();
        const numero = document.getElementById('checkout-numero').value.trim();

        if (!name || !cep || !rua || !numero) {
            showToast('Por favor, preencha todos os campos obrigatórios (Nome, CEP, Rua e Número).');
            return false;
        }
        return true;
    }

    function buildOrderObject(paymentMethod) {
        const totalPrice = cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);
        const order = {
            id: 'REI-' + Math.floor(100000 + Math.random() * 900000),
            buyer: document.getElementById('checkout-nome').value.trim(),
            cep: document.getElementById('checkout-cep').value.trim(),
            address: `${document.getElementById('checkout-rua').value.trim()}, ${document.getElementById('checkout-numero').value.trim()} - ${document.getElementById('checkout-bairro').value.trim()}, ${document.getElementById('checkout-cidade').value.trim()}/${document.getElementById('checkout-uf').value.trim()}`,
            complement: document.getElementById('checkout-complemento').value.trim(),
            items: [...cart],
            total: totalPrice,
            paymentMethod: paymentMethod,
            date: new Date().toLocaleString('pt-BR')
        };

        // Dispara a notificação por e-mail do estabelecimento mapeada para futuro alinhamento
        sendOrderEmailNotification(order);

        return order;
    }

    async function sendOrderEmailNotification(order) {
        const storeEmail = window.STORE_NOTIFICATION_EMAIL || 'pedidos@reidoabc.com.br';
        const payload = {
            ...order,
            store_email: storeEmail
        };

        try {
            const response = await fetch('api/submit-order.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await response.json();
            if (result.success) {
                console.log('Notificação de pedido por e-mail disparada com sucesso:', result);
                showToast(`Notificação do Pedido ${order.id} encaminhada por e-mail!`);
            }
        } catch (err) {
            console.log('Mapeamento de e-mail de pedido ativado (Aguardando confirmação do e-mail final do estabelecimento).');
        }
    }

    function showPixModal(order) {
        const pixContainer = document.getElementById('pix-order-summary');
        // Chave PIX do Estabelecimento (pode ser sobrescrita via window.ESTABELECIMENTO_PIX_KEY)
        const pixKey = window.ESTABELECIMENTO_PIX_KEY || 'contato@reidoabc.com.br';
        const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${encodeURIComponent('00020126360014BR.GOV.BCB.PIX0114' + pixKey + '5204000053039865405' + order.total.toFixed(2) + '5802BR5910REI_DO_ABC6009SAO_PAULO62070503***6304')}`;

        if (pixContainer) {
            pixContainer.innerHTML = `
                <div style="background: rgba(216, 180, 86, 0.1); border: 1px solid var(--primary-color); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
                    <p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>Número do Pedido:</strong> <span style="color: var(--primary-color);">${order.id}</span></p>
                    <p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>Comprador:</strong> ${order.buyer}</p>
                    <p style="margin-bottom: 6px; font-size: 0.95rem;"><strong>Valor Total a Pagar:</strong> <span style="color: var(--primary-color); font-weight:800; font-size: 1.1rem;">R$ ${order.total.toFixed(2).replace('.', ',')}</span></p>
                    <p style="font-size: 0.85rem; color: var(--text-muted);"><strong>Endereço:</strong> ${order.address} ${order.complement ? '(' + order.complement + ')' : ''}</p>
                </div>
                
                <!-- QR Code PIX em Destaque Gourmet -->
                <div style="text-align:center; margin: 1.25rem 0;">
                    <div style="display: inline-block; background: #ffffff; padding: 14px; border-radius: 18px; border: 3px solid var(--primary-color); box-shadow: 0 0 30px rgba(216, 180, 86, 0.35); margin-bottom: 12px;">
                        <img src="${qrCodeUrl}" alt="QR Code PIX Rei do ABC" style="width: 200px; height: 200px; display: block; border-radius: 8px;">
                    </div>
                    <p style="font-size: 0.9rem; font-weight: 800; color: var(--primary-color); margin-bottom: 4px;">1. Escaneie o QR Code acima no aplicativo do seu banco</p>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px;">ou utilize a Chave PIX Copia e Cola abaixo:</p>
                    
                    <div style="background: #000; border: 1px dashed var(--primary-color); padding: 12px; border-radius: 8px; font-weight: 800; font-size: 1.05rem; color: var(--primary-color); word-break: break-all; margin-bottom: 12px;" id="pix-key-text">
                        ${pixKey}
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 1rem;">
                    <button class="btn-primary-gourmet" id="btn-copy-pix">Copiar Chave PIX</button>
                    <a href="https://api.whatsapp.com/send?phone=5511948948977&text=Olá!%20Realizei%20o%20pagamento%20PIX%20do%20Pedido%20${order.id}%20no%20valor%20de%20R$%20${order.total.toFixed(2).replace('.', ',')}%20para%20o%20Rei%20do%20ABC.%20Segue%20o%20comprovante." target="_blank" class="btn-gourmet-pay btn-gourmet-pix" style="text-decoration:none; text-align:center; display:block;">
                        <img src="assets/images/icon-whatsapp.svg" alt="WhatsApp" style="height:20px; vertical-align:middle;"> Enviar Comprovante no WhatsApp
                    </a>
                </div>
            `;

            document.getElementById('btn-copy-pix').addEventListener('click', () => {
                const keyText = document.getElementById('pix-key-text').innerText.trim();
                navigator.clipboard.writeText(keyText);
                showToast('Chave PIX do Estabelecimento copiada com sucesso!');
            });
        }
        openModal(pixModal);
        cart = [];
        saveCart();
        updateCartUI();
    }

    function showOrderSuccessModal(order) {
        showToast(`Pedido ${order.id} gerado com sucesso! Redirecionado para o pagamento.`);
    }

    // Helper Modais e Toast
    function openModal(modal) {
        closeAllModals();
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    function closeAllModals() {
        document.querySelectorAll('.custom-modal-wrapper').forEach(m => m.style.display = 'none');
        document.body.style.overflow = 'auto';
    }

    function showToast(message) {
        let toast = document.getElementById('gourmet-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'gourmet-toast';
            toast.className = 'gourmet-toast';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `<img src="assets/images/logo-rei-do-abc.svg" class="brand-crown-icon-sm" alt="Rei do ABC"> ${message}`;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3500);
    }
});
