describe('Generate flow', () => {
  it('submits a prompt and shows preview', () => {
    cy.intercept('POST', '/generate', { job_id: '123' }).as('post');
    cy.intercept('GET', '/generate/123', {
      png_url: '/test.png',
      ldr_url: null,
      gltf_url: null,
      brick_counts: {},
    }).as('get');
    cy.visit('/');
    cy.get('input[required]').type('castle');
    cy.contains('button', 'Generate').click();
    cy.wait('@post');
    cy.wait('@get');
    cy.get('img[src="/test.png"]').should('be.visible');
  });
});
