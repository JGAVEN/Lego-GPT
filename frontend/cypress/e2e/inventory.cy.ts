describe('inventory scan', () => {
  it('uploads photo and generates with detected inventory', () => {
    cy.intercept('POST', '/detect_inventory', { job_id: '1' }).as('detectPost');
    cy.intercept('GET', '/detect_inventory/1', {
      statusCode: 200,
      body: { brick_counts: { '3001.DAT': 1 } },
    }).as('detectGet');

    cy.intercept('POST', '/generate', (req) => {
      expect(req.body.inventory_filter).to.deep.equal({ '3001.DAT': 1 });
      req.reply({ job_id: '2' });
    }).as('genPost');
    cy.intercept('GET', '/generate/2', {
      statusCode: 200,
      body: {
        png_url: '/static/x/preview.png',
        ldr_url: null,
        gltf_url: null,
        brick_counts: { '3001.DAT': 1 },
      },
    }).as('genGet');

    cy.visit('/');
    cy.fixture('lego.txt').then((b64) => {
      const blob = Cypress.Buffer.from(b64.trim(), 'base64');
      cy.get('input[type=file]').selectFile({ contents: blob, fileName: 'lego.png' });
    });
    cy.wait('@detectPost');
    cy.wait('@detectGet');
    cy.contains('Detected Inventory');
    cy.get('button[type=submit]').click();
    cy.wait('@genPost');
    cy.wait('@genGet');
    cy.get('img[alt="Lego preview"]');
  });
});
