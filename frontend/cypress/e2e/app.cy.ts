describe('Lego GPT PWA', () => {
  it('loads the home page', () => {
    cy.visit('/');
    cy.contains('Lego GPT Demo');
  });

  it('submits a generate request', () => {
    cy.intercept('POST', '/generate', { job_id: '1' }).as('generate');
    cy.visit('/');
    cy.get('input[required]').type('a house');
    cy.get('button[type="submit"]').click();
    cy.wait('@generate');
  });
});
