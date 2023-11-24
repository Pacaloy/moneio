document.addEventListener('DOMContentLoaded', () => {
  const endpoint = window.location.pathname.split('/');
  const params = {
    username: endpoint[1],
    moneio: endpoint[2],
    accountId: endpoint[3],
  };
  document.querySelector('#cancelEditMoneioBtn').onclick = goToRootPage;
  document.querySelector('#deleteMoneioBtn').onclick = () => deleteTransaction(params);

  document.querySelector('#form-moneio').onsubmit = () => {
    saveEditTransaction(params);
    return false
  };
});

function goToRootPage() {
  window.location = '/';
}

function saveEditTransaction(params) {
  fetch(`/${params.username}/${params.moneio}/${params.accountId}`, {
    method: 'PUT',
    body: JSON.stringify({
      name: document.querySelector('#formMoneioName').value,
      price: document.querySelector('#formMoneioMoney').value,
      date: document.querySelector('#formMoneioDate').value,
      account: document.querySelector('#formMoneioAccount').value,
    }),
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}

function deleteTransaction(params) {
  fetch(`/${params.username}/${params.moneio}/${params.accountId}`, {
    method: 'DELETE',
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}
