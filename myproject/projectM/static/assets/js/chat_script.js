//const csrfToken = '{{ csrf_token }}';
$(document).ready(function () {
    const slug = $('#chat-container').data('slug');
    const csrfToken = $('#chat-container').data('csrf');

    $('#user-input').keypress(function (e) {
        if (e.which === 13) sendMessage();
    });

    window.sendMessage = function () {
        const userInput = $('#user-input').val();
        if (userInput.trim() === '') return;

        $('#chat-messages').append(
            `<div class="message user-message"><p>${userInput}</p></div>`
        );
        $('#user-input').val('');
        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

        $.ajax({
    url: `/services/chatbot/${slug}/`,
    type: 'POST',
    data: {
        'message': userInput,
        'csrfmiddlewaretoken': csrfToken
    },
    success: function (response) {
        $('#chat-messages').append(
            `<div class="message bot-message"><p>${response.message}</p></div>`
        );
        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
    },
    error: function (xhr, status, error) {
        console.error("Error:", error);
        $('#chat-messages').append(
            `<div class="message bot-message"><p><em>Bot is not responding.</em></p></div>`
        );
    }
});

    };
});

//----------------------------------------------------

//  $(document).ready(function () {
//     $('#user-input').keypress(function (e) {
//         if (e.which === 13) {
//             sendMessage();
//         }
//     });

//     window.sendMessage = function () {
//         const userInput = $('#user-input').val();
//         if (userInput.trim() !== '') {
//             $('#chat-messages').append(
//                 '<div class="message user-message"><p>' + userInput + '</p></div>'
//             );
//             $('#user-input').val('');
//             $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

//             $.ajax({
//                 url: "{% url 'projectM:chatbot' slug=slug %}",  // If used inside template
//                 type: 'POST',
//                 data: {
//                     'message': userInput,
//                     'csrfmiddlewaretoken': '{{ csrf_token }}' // Must be in template
//                 },
//                 success: function (response) {
//                     $('#chat-messages').append(
//                         '<div class="message bot-message"><p>' + response.message + '</p></div>'
//                     );
//                     $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
//                 }
//             });
//         }
//     }
// });

 //---------------------------------------------------------------------
 
 // function sendMessage() {
  //   var userInput = $('#user-input').val();
  //   if (userInput.trim() !== '') {
  //     $('#chat-messages').append(
  //       '<div class="message user-message"><p>' + userInput + '</p></div>'
  //     );
  //     $('#user-input').val('');
  //     $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);

  //     $.ajax({
  //       url: "{% url 'projectM:chatbot' slug=slug %}",
  //       type: 'POST',
  //       data: {
  //         'message': userInput,
  //         'csrfmiddlewaretoken': '{{ csrf_token }}'
  //       },
  //       success: function (response) {
  //         $('#chat-messages').append(
  //           '<div class="message bot-message"><p>' + response.message + '</p></div>'
  //         );
  //         $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
  //       }
  //     });
  //   }
  // }

  // $('#user-input').keypress(function (e) {
  //   if (e.which === 13) {
  //     sendMessage();
  //   }
  // });