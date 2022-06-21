// I thought I could just do it without React.
// In the end, I realized I should have done it with React.

let data = []; // [0] name, [1] women, [2] men, [3] sum, [4] rank
const interval = 100;
let from = 0;
let to = interval;

function checkGender(tr, women, men) {
  return (women && tr[1].length > 1) || (men && tr[2].length > 1);
}

function buildRows(fromNew, toNew) {
  const women = $('#women').prop('checked');
  const men = $('#men').prop('checked');
  const trs = [];
  for (let i = fromNew; i < toNew; i += 1) {
    const tr = data[i];
    if (checkGender(tr, women, men)) {
      let gender = '⚤';
      if (tr[1] === '0') {
        gender = '♂';
      } else if (tr[2] === '0') {
        gender = '♀';
      }
      const svg = `<svg width='100' height='10'><rect width='${parseFloat(tr[3]) / 100.0}' height='10' fill='#c5e7ed'></rect></svg>`;
      const $tr = $(`<tr id='row-${i}'><td>${tr[4]}.</td><td>${gender}</td><td>${tr[0]}</td><td>${tr[3]}</td><td>${svg}</td></tr>`);
      trs.push($tr);
    }
  }
  return trs;
}

function buildTable() {
  $('#table table').empty();
  const rows = buildRows(from, to);
  if (rows.length) {
    rows.forEach(x => $('#table table').append(x));
  } else {
    $('#table table').html('Nothing to show!');
    $('#up').css('visibility', 'hidden');
    $('#down').css('visibility', 'hidden');
  }
}

function setUpData(json) {
  data = json;
  buildTable();
}

function search(query) {
  const women = $('#women').prop('checked');
  const men = $('#men').prop('checked');
  for (let i = 0; i < data.length; i += 1) {
    const tr = data[i];
    if (checkGender(tr, women, men)) {
      if (data[i][0].toLowerCase().startsWith(query.toLowerCase())) {
        return i;
      }
    }
  }
  return -1;
}

function handleSearch() {
  const query = $('#searchText').val();
  const index = search(query);
  if (index >= 0 && (query !== '')) {
    from = Math.max(0, index);
    to = Math.min(data.length - 1, from + interval);
    buildTable();
    if (from > 0) {
      $('#up').css('visibility', 'visible');
    }
  } else if (query === '') {
    from = 0;
    to = interval;
    buildTable();
    $('#up').css('visibility', 'hidden');
    $('#down').css('visibility', 'visible');
  } else {
    $('#table table').html('Nothing found!');
    $('#up').css('visibility', 'hidden');
    $('#down').css('visibility', 'hidden');
  }

  if (query !== '') {
    $('tr td:nth-child(3)').each((i, v) => {
      const tdValue = $(v).html();
      if (tdValue.toLowerCase().startsWith(query.toLowerCase())) {
        $(v).parent().addClass('fat');
      }
    });
  }
}

function handleSearchEvent(event) {
  event.preventDefault();
  handleSearch();
  return false;
}

function showMoreUp() {
  // circumvent scrolling to top
  const oldHeight = $(document).height();
  const oldScroll = $(window).scrollTop();
  const fromNew = Math.max(0, from - interval);
  buildRows(fromNew, from).reverse().forEach(x => $('#table table').prepend(x));
  $(document).scrollTop((oldScroll + $(document).height()) - oldHeight);

  from = fromNew;
  if (from === 0) {
    $('#up').css('visibility', 'hidden');
  }
}

function showMoreDown() {
  const toNew = Math.min(data.length - 1, to + interval);
  buildRows(to, toNew).forEach(x => $('#table table').append(x));

  to = toNew;
  if (to === data.length - 1) {
    $('#down').css('visibility', 'hidden');
  }
}

function handleGenderSelectionChange() {
  handleSearch();
}

export default function init() {
  $.getJSON('./data.json', setUpData);
  $('#women').change(handleGenderSelectionChange);
  $('#men').change(handleGenderSelectionChange);
  $('#searchText').on('input', handleSearchEvent);
  $('#up').click(showMoreUp);
  $('#down').click(showMoreDown);
}
