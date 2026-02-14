const API_BASE_URL = 'https://proyectociber.onrender.com';
const sections = {
    list: document.getElementById('user-list-container'),
    getById: document.getElementById('get-user-by-id-form'),
    update: document.getElementById('update-user-form'),
    delete: document.getElementById('delete-user-form')
};

function showSection(key) {
    Object.values(sections).forEach(s => s?.classList.add('hidden'));
    sections[key].classList.remove('hidden');
}

function renderUserRow(user) {
    const isActive = user.detalles?.[0]?.estado_cuenta;
    const initials = user.nombre ? user.nombre.substring(0, 2).toUpperCase() : '??';
    
    return `
        <tr class="hover:bg-gray-50/50 transition-colors group">
            <td class="px-8 py-5"><input type="checkbox" class="rounded border-gray-300"></td>
            <td class="px-8 py-5">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center font-bold text-gray-600 border border-gray-200 text-xs">${initials}</div>
                    <div>
                        <div class="font-bold text-gray-900">${user.nick_name}</div>
                        <div class="text-gray-400 text-xs font-medium">ID: ${user.id_usuario}</div>
                    </div>
                </div>
            </td>
            <td class="px-8 py-5">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-bold ${isActive ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'}">
                    <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-green-500' : 'bg-gray-400'}"></span>
                    ${isActive ? 'ACTIVE' : 'INACTIVE'}
                </span>
            </td>
            <td class="px-8 py-5 text-gray-500 font-medium">${user.detalles?.[0]?.grupo || 'Member'}</td>
            <td class="px-8 py-5 text-gray-400">${user.detalles?.[0]?.email || 'N/A'}</td>
            <td class="px-8 py-5 text-right">
                <div class="flex gap-3 justify-end opacity-0 group-hover:opacity-100 transition-opacity text-gray-400">
                    <button class="hover:text-blue-500"><i data-lucide="edit-2" class="w-4 h-4"></i></button>
                    <button class="hover:text-red-500"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                </div>
            </td>
        </tr>`;
}

// LÓGICA DE EVENTOS
document.getElementById('get-all-users').addEventListener('click', () => {
    showSection('list');
    fetch(`${API_BASE_URL}/usuarios/`)
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('user-table-body');
            tbody.innerHTML = data.map(user => renderUserRow(user)).join('');
            document.getElementById('user-count').textContent = data.length;
            lucide.createIcons();
        });
});

document.getElementById('get-user-by-id').addEventListener('click', () => showSection('getById'));

const getUserBtn = document.getElementById('get-user-by-id-button');
getUserBtn.addEventListener('click', () => {
    const id = document.getElementById('user-id-input').value;
    const msg = document.getElementById('message-get-user');
    const resContainer = document.getElementById('result-container');
    
    msg.textContent = "Searching...";
    resContainer.classList.add('hidden');

    fetch(`${API_BASE_URL}/usuarios/${id}`)
        .then(r => r.ok ? r.json() : Promise.reject('User not found'))
        .then(user => {
            document.getElementById('single-user-result').innerHTML = renderUserRow(user);
            resContainer.classList.remove('hidden');
            msg.textContent = "";
            lucide.createIcons();
        })
        .catch(err => {
            msg.innerHTML = `<span class="text-red-600">${err}</span>`;
        });
});

document.getElementById('update-user').addEventListener('click', () => showSection('update'));

// --- LÓGICA DE UPDATE ---
document.getElementById('update-user-button').addEventListener('click', () => {
    const userId = document.getElementById('update-user-id').value;
    const msg = document.getElementById('message-update-user');
    
    const userData = {
        nick_name: document.getElementById('update-nick_name').value || undefined,
        nombre: document.getElementById('update-nombre').value || undefined,
        email: document.getElementById('update-email').value || undefined
    };

    // Limpiar campos vacíos para no enviar nulls innecesarios
    Object.keys(userData).forEach(key => userData[key] === undefined && delete userData[key]);

    if (!userId) {
        msg.innerHTML = `<span class="text-red-600">⚠️ ID is required to update.</span>`;
        return;
    }

    fetch(`${API_BASE_URL}/usuarios/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(r => r.ok ? r.json() : Promise.reject('Update failed. Check ID.'))
    .then(data => {
        msg.innerHTML = `<span class="text-green-600 font-bold">✅ User ${userId} updated successfully!</span>`;
        lucide.createIcons();
    })
    .catch(err => {
        msg.innerHTML = `<span class="text-red-600">❌ ${err}</span>`;
    });
});

document.getElementById('delete-user').addEventListener('click', () => showSection('delete'));

// --- LÓGICA DE DELETE ---
document.getElementById('delete-user-button').addEventListener('click', () => {
    const userId = document.getElementById('delete-user-id-input').value;
    const msg = document.getElementById('message-delete-user');

    if (!userId) {
        msg.innerHTML = `<span class="text-red-600">⚠️ Please provide a valid ID.</span>`;
        return;
    }

    if (!confirm(`Are you sure you want to delete user ${userId}?`)) return;

    fetch(`${API_BASE_URL}/usuarios/${userId}`, { method: 'DELETE' })
    .then(r => r.ok ? r.json() : Promise.reject('Delete failed. User might not exist.'))
    .then(() => {
        msg.innerHTML = `<span class="text-green-600 font-bold">🗑️ User ${userId} has been removed.</span>`;
        document.getElementById('delete-user-id-input').value = '';
    })
    .catch(err => {
        msg.innerHTML = `<span class="text-red-600">❌ ${err}</span>`;
    });
});
// Inicializar iconos
lucide.createIcons();