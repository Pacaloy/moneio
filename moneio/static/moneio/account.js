document.addEventListener('DOMContentLoaded', () => {
  const endpoint = window.location.pathname.split('/');
  const params = {
    username: endpoint[1],
    account: endpoint[2],
    accountId: endpoint[3],
  };
  document.querySelector('#cancelEditAccountBtn').onclick = goToRootPage;
  document.querySelector('#deleteAccountBtn').onclick = () => deleteAccount(params);

  document.querySelector('#form-account').onsubmit = () => {
    saveEditAccount(params);
    return false
  };
});

function goToRootPage() {
  window.location = '/';
}

function saveEditAccount(params) {
  fetch(`/${params.username}/${params.account}/${params.accountId}`, {
    method: 'PUT',
    body: JSON.stringify({
      name: document.querySelector('#formAccountName').value,
      balance: document.querySelector('#formAccountInitialBalance').value,
      date: document.querySelector('#formAccountDate').value,
    }),
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}

function deleteAccount(params) {
  fetch(`/${params.username}/${params.account}/${params.accountId}`, {
    method: 'DELETE',
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}
