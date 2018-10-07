export function selectCard(line_id) {
  return {
    type: 'SELECT_CARD',
    line_id
  }
}

export function deselectCard(line_id) {
  return {
    type: 'DESELECT_CARD',
    line_id
  }
}