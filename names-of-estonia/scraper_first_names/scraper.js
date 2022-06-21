/*
 * This is a JavaScript Scratchpad.
 *
 * Enter some JavaScript, then Right Click or choose from the Execute Menu:
 * 1. Run to evaluate the selected text (Cmd-R),
 * 2. Inspect to bring up an Object Inspector on the result (Cmd-I), or,
 * 3. Display to insert the result in a comment after the selection. (Cmd-L)
 */

let xxdata = ['dfdf', 'jul', 'joh'];

// for(let i = 0; i < xxdata.length; i++) {
  
//   (function(i){
//       console.log(name);
  
//       const text = document.getElementById('tulemus').getElementsByClassName('fldvalue')[0].childNodes[0].nodeValue;
// //       localStorage.setItem(name, text);
//       console.log(text);
//   }(i));
// }

let i = 0;
setInterval(function() {
     const text = document.getElementById('tulemus').getElementsByClassName('fldvalue')[0].childNodes[0].nodeValue;
     console.log(text);
  
    const name = xxdata[i];
    document.getElementsByName('enimi')[0].value = name;
//     document.getElementsByName('esita')[0].click();
    i++;
}, 5000);
