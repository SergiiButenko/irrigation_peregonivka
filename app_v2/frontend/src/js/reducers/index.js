function selectedCardsCounter(state = [], action) {
  switch (action.type) {
    case 'SELECT_CARD':
      return state.concat([action.line_id])
    case 'DESELECT_CARD':
      return state.filter(e => e !== action.line_id)
    default:
      return state
  }
}

export default selectedCardsCounter;
