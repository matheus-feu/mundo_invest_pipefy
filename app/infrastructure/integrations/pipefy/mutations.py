CREATE_CARD_MUTATION = """
mutation CreateCard($input: CreateCardInput!) {
  createCard(input: $input) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_MUTATION = """
mutation UpdateCard($input: UpdateCardInput!) {
  updateCard(input: $input) {
    card {
      id
    }
  }
}
"""