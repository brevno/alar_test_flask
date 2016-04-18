var closeDialogs = function(callbackAfterClose) {
    var activeDialogs = $('.dialog.active');
    if (activeDialogs.length) {
        activeDialogs.fadeOut({
            done: callbackAfterClose
        });
     } else if (callbackAfterClose) {
        callbackAfterClose();
    }
}

var callAPI = function(url, formData) {
    $.post(url, formData)
        .done(function (data) {
            if (data.status === 'error') {
                showErrorDialog(data.errors);
            } else if (data.status === 'OK') {
                location.reload();
            }
        })

};

var showEditForm = function(e) {
    var data = {};
    data.userId = $(e.currentTarget).closest('tr').find('.user-id').get(0).innerHTML;
    data.name = $(e.currentTarget).closest('tr').find('.user-name').get(0).innerHTML;
    data.isAdmin = $(e.currentTarget).closest('tr').find('.user-is-admin').get(0).innerHTML;

    closeDialogs(function () {
        $('#edit-user').fadeIn().addClass('active');
    });

    $('#edit-user #user_id').val(data.userId);
    $('#edit-user #name').val(data.name);
    $('#edit-user #is_admin').prop('checked', data.isAdmin === 'yes');
};

var showNewUserForm = function(e) {
    closeDialogs(function () {
        $('#new-user').fadeIn().addClass('active');
    });
};

var showNewPasswordForm = function(e) {
    var userId = $(e.currentTarget).closest('tr').find('.user-id').get(0).innerHTML;

    closeDialogs(function () {
        $('#new-password').fadeIn().addClass('active');
    });

    $('#new-password #user_id').val(userId);
};

var showDeleteConfirmation = function(e) {
    var data = {};
    data.userId = $(e.currentTarget).closest('tr').find('.user-id').get(0).innerHTML;
    data.name = $(e.currentTarget).closest('tr').find('.user-name').get(0).innerHTML;

    closeDialogs(function () {
        $('#confirm-delete').fadeIn().addClass('active');
    });

    $('#confirm-delete #user_id').val(data.userId);
    $('#confirm-delete .header span').get(0).innerHTML = data.name;
};

var showErrorDialog = function(errors) {
    closeDialogs(function () {
        $('#error-msg').fadeIn().addClass('active');
    });

    $('#error-msg .errors-list').get(0).innerHTML = '';
    var errorHTML = '';
    for (var name in errors) {
        errorHTML += name + ': ' + errors[name] + '<br>';
    }
    $('#error-msg .errors-list').get(0).innerHTML = errorHTML;
};

var sendEditData = function (e) {
    var formData = $('#edit-user form').serialize();
    callAPI('/edit_user',formData);
};

var sendNewPasswordData = function (e) {
    var formData = $('#new-password form').serialize();
    callAPI('/new_password',formData);
};

var sendNewUserData = function (e) {
    var formData = $('#new-user form').serialize();
    callAPI('/new_user',formData);
};

var sendDeleteUser = function (e) {
    var formData = $('#confirm-delete form').serialize();
    callAPI('/delete_user',formData);
};

var bindEventHandlers = function () {
    $('tr.data-row i.edit').on('click', function(e) {
        showEditForm(e);
    });
    $('tr.data-row i.password').on('click', function(e) {
        showNewPasswordForm(e);
    });
    $('tr.data-row i.delete').on('click', function(e) {
        showDeleteConfirmation(e);
    });
    $('#btn-new-user').on('click', function(e) {
        showNewUserForm(e);
    });
    $('#edit-user .btn-ok').on('click', function(e) {
        sendEditData(e);
    });
    $('#new-user .btn-ok').on('click', function(e) {
        sendNewUserData(e);
    });
    $('#new-password .btn-ok').on('click', function(e) {
        sendNewPasswordData(e);
    });
    $('#confirm-delete .btn-ok').on('click', function(e) {
        sendDeleteUser(e);
    });
    $('#error-msg button').on('click', function(e) {
        closeDialogs();
    });
    $('.btn-cancel').on('click', function(e) {
        closeDialogs();
    });
    $('body').on('keyup', function(e) {
        if (e.keyCode === 27) {
            closeDialogs();
        }
    });
    $('input').on('keypress', function(e) {
        if (e.keyCode !== 13) {
            return;
        }
        e.preventDefault();

        // try to find 'OK' button in parent form and trigger it's click
        var $buttons = $(e.currentTarget).closest('form').find('button');
        if ($buttons && $buttons.length) {
            $buttons.get(0).click();
        }
    });
};

$(bindEventHandlers);
