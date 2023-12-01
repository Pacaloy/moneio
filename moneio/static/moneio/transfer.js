document.addEventListener('DOMContentLoaded', () => {
  const endpoint = window.location.pathname.split('/');
  const params = {
    username: endpoint[1],
    transfer: endpoint[2],
    accountId: endpoint[3],
  };
  document.querySelector('#cancelEditTransferBtn').onclick = goToRootPage;
  document.querySelector('#deleteTransferBtn').onclick = () => deleteTransfer(params);

  document.querySelector('#form-transfer').onsubmit = () => {
    saveEditTransfer(params);
    return false
  };
});

function goToRootPage() {
  window.location = '/';
}

function saveEditTransfer(params) {
  fetch(`/${params.username}/${params.transfer}/${params.accountId}`, {
    method: 'PUT',
    body: JSON.stringify({
      name: document.querySelector('#formTransferName').value,
      price: document.querySelector('#formTransferMoney').value,
      fromAccount: document.querySelector('#formFromAccount').value,
      toAccount: document.querySelector('#formToAccount').value,
      date: document.querySelector('#formTransferDate').value,
    }),
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}

function deleteTransfer(params) {
  fetch(`/${params.username}/${params.transfer}/${params.accountId}`, {
    method: 'DELETE',
  })
  .then(() => {
    setTimeout(() => {
      goToRootPage();
    }, 300)
  });
}
