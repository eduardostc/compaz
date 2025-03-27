var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
onKeyPress: function(val, e, field, options) {
    field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};


$(function(){
    $('.mask-telefone').mask(SPMaskBehavior, spOptions);
});




// document.addEventListener('DOMContentLoaded', function() {
//     // Verifica se jQuery está carregado
//     if(typeof jQuery === 'undefined') {
//         console.error('jQuery não está carregado!');
//         return;
//     }
    
//     // Verifica se o plugin de máscara está carregado
//     if(typeof jQuery.fn.mask === 'undefined') {
//         console.error('jQuery Mask Plugin não está carregado!');
//         return;
//     }

//     // Define o comportamento da máscara
//     var SPMaskBehavior = function (val) {
//         return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
//     };

//     var spOptions = {
//         onKeyPress: function(val, e, field, options) {
//             field.mask(SPMaskBehavior.apply({}, arguments), options);
//         }
//     };

//     // Aplica a máscara
//     $('.mask-telefone').mask(SPMaskBehavior, spOptions);
    
//     console.log('Máscara de telefone inicializada'); // Para debug
// });