function initQuillEditor(editorId, contentInputId, formId, initialContent = '') {
    // Kontrola, zda editor již existuje, a pokud ano, zničíme ho
    const editorElement = document.getElementById(editorId);
    if (editorElement && editorElement.__quill) {
        editorElement.__quill = null;
    }

    // Vlastní ikona pro tlačítko formula
    const icons = Quill.import('ui/icons');
    icons.formula = '<span style="font-weight: bold; font-size: 16px;">Σ</span>';

    // Inicializace editoru s KaTeX modulem
    const quill = new Quill(`#${editorId}`, {
        modules: {
            formula: true, // Aktivujeme vestavěný modul pro formule
            toolbar: {
                container: [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'header': 1 }, { 'header': 2 }],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'script': 'sub' }, { 'script': 'super' }],
                    [{ 'indent': '-1' }, { 'indent': '+1' }],
                    [{ 'size': ['small', false, 'large', 'huge'] }],
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'font': [] }],
                    [{ 'align': [] }],
                    ['clean'],
                    ['formula'] // Použijeme vestavěné tlačítko pro formule
                ],
                handlers: {
                    'formula': function() {
                        // Získáme aktuální pozici kurzoru
                        const range = quill.getSelection();
                        if (range) {
                            // Zobrazíme vlastní modální okno pro zadání formule
                            showFormulaModal(function(formula) {
                                if (formula) {
                                    // Vložíme formuli na pozici kurzoru
                                    quill.insertEmbed(range.index, 'formula', formula, Quill.sources.USER);
                                    // Posuneme kurzor za formuli
                                    quill.setSelection(range.index + 1, 0, Quill.sources.USER);
                                }
                            });
                        }
                    }
                }
            },
            history: {
                delay: 1000,
                maxStack: 100,
                userOnly: true
            }
        },
        placeholder: 'Enter text ...',
        theme: 'snow'
    });

    // Přidáme posluchač událostí pro kliknutí na formuli
    quill.root.addEventListener('click', function(e) {
        // Najdeme nejbližší formuli
        const formulaElement = e.target.closest('.ql-formula');
        if (formulaElement) {
            // Získáme index formule v editoru
            const blot = Quill.find(formulaElement);
            if (blot) {
                const index = quill.getIndex(blot);
                if (index !== -1) {
                    // Nastavíme kurzor za formuli
                    quill.setSelection(index + 1, 0, Quill.sources.USER);
                }
            }
        }
    });

    // Uložení reference na editor do elementu
    editorElement.__quill = quill;

    // Pokud je k dispozici počáteční obsah, nastavte ho
    if (initialContent) {
        try {
            quill.clipboard.dangerouslyPasteHTML(initialContent);
        } catch (e) {
            console.error("Error setting initial content:", e);
            // Záložní metoda, pokud dangerouslyPasteHTML selže
            quill.root.innerHTML = initialContent;
        }
    }

    // Při odesílání formuláře - tato část musí zůstat zachována
    const form = document.getElementById(formId);
    const oldSubmitHandler = form._quillSubmitHandler;
    if (oldSubmitHandler) {
        form.removeEventListener('submit', oldSubmitHandler);
    }
    
    // Získání HTML obsahu z editoru
    const submitHandler = function (e) {
        const editorContent = quill.root.innerHTML;
        // Nastavení hodnoty skrytého inputu
        document.getElementById(contentInputId).value = editorContent;
    };

    // Uložení reference na handler pro pozdější odstranění
    form._quillSubmitHandler = submitHandler;
    form.addEventListener('submit', submitHandler);

    // Přidáme styly pro lepší zobrazení formule
    const formulaStyle = document.createElement('style');
    formulaStyle.textContent = `
        .ql-formula {
            display: inline-block;
            vertical-align: middle;
            margin: 0 2px;
            cursor: pointer;
        }
        
        /* Přidáme mezeru za formuli pro lepší umístění kurzoru */
        .ql-formula::after {
            content: '';
            display: inline-block;
            width: 2px;
            height: 1em;
        }
        
        /* Styly pro modální okno formule */
        .formula-modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 500px;
            max-width: 90%;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 9999;
            padding: 20px;
        }
        
        .formula-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 9998;
        }
        
        .formula-input-container {
            margin: 15px 0;
        }
        
        #formula-input {
            width: 100%;
            height: 80px;
            padding: 8px;
            font-family: monospace;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        .formula-preview {
            margin: 15px 0;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 4px;
            min-height: 50px;
        }
        
        .formula-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        
        .formula-buttons button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        #formula-cancel {
            background-color: #f0f0f0;
        }
        
        #formula-insert {
            background-color: #007bff;
            color: white;
        }
        
        @media (prefers-color-scheme: dark) {
            .formula-modal {
                background-color: #333;
                color: white;
            }
            
            #formula-input {
                background-color: #222;
                color: white;
                border-color: #444;
            }
            
            .formula-preview {
                border-color: #444;
                background-color: #222;
            }
            
            #formula-cancel {
                background-color: #555;
                color: white;
            }
        }
    `;
    document.head.appendChild(formulaStyle);

    // Funkce pro zobrazení modálního okna pro zadání LaTeX vzorce
    function showFormulaModal(callback) {
        // Odstraníme existující modální okno, pokud existuje
        const existingModal = document.querySelector('.formula-modal');
        const existingOverlay = document.querySelector('.formula-modal-overlay');
        if (existingModal) {
            document.body.removeChild(existingModal);
        }
        if (existingOverlay) {
            document.body.removeChild(existingOverlay);
        }
        
        // Vytvoříme overlay
        const overlay = document.createElement('div');
        overlay.className = 'formula-modal-overlay';
        document.body.appendChild(overlay);
        
        // Vytvoříme modální okno
        const modal = document.createElement('div');
        modal.className = 'formula-modal';
        modal.innerHTML = `
            <h4>Vložit LaTeX vzorec</h4>
            <div class="formula-input-container">
                <textarea id="formula-input" placeholder="Např. E = mc^2"></textarea>
            </div>
            <div class="formula-preview">
                <h5>Náhled:</h5>
                <div id="formula-preview"></div>
            </div>
            <div class="formula-buttons">
                <button type="button" id="formula-cancel">Zrušit</button>
                <button type="button" id="formula-insert">Vložit</button>
            </div>
        `;
        document.body.appendChild(modal);

        // Získáme reference na elementy
        const formulaInput = document.getElementById('formula-input');
        const formulaPreview = document.getElementById('formula-preview');
        const cancelButton = document.getElementById('formula-cancel');
        const insertButton = document.getElementById('formula-insert');

        // Přidáme posluchače událostí
        formulaInput.addEventListener('input', updatePreview);
        cancelButton.addEventListener('click', closeModal);
        insertButton.addEventListener('click', insertFormula);
        overlay.addEventListener('click', closeModal);

        // Přidání podpory pro klávesové zkratky
        formulaInput.addEventListener('keydown', function (e) {
            // Enter s Ctrl nebo Cmd vloží formuli
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                insertFormula();
            }
            // Escape zruší vkládání
            else if (e.key === 'Escape') {
                e.preventDefault();
                closeModal();
            }
        });

        // Funkce pro aktualizaci náhledu
        function updatePreview() {
            const formula = formulaInput.value.trim();
            if (formula) {
                try {
                    katex.render(formula, formulaPreview, {
                        throwOnError: false
                    });
                } catch (e) {
                    formulaPreview.textContent = 'Chyba v syntaxi LaTeX';
                }
            } else {
                formulaPreview.textContent = '';
            }
        }

        // Funkce pro zavření modálního okna
        function closeModal() {
            document.body.removeChild(modal);
            document.body.removeChild(overlay);
        }

        // Funkce pro vložení vzorce
        function insertFormula() {
            const formula = formulaInput.value.trim();
            closeModal();
            callback(formula);
        }

        // Zaměřte se na vstupní pole
        formulaInput.focus();
    }

    return quill;
}

//Zajistíme, že se funkce nespustí vícekrát pro stejný editor
window.initedEditors = window.initedEditors || {};
const originalInitQuillEditor = initQuillEditor;
initQuillEditor = function (editorId, contentInputId, formId, initialContent = '') {
    if (window.initedEditors[editorId]) {
        console.log(`Editor ${editorId} already initialized, skipping`);
        return window.initedEditors[editorId];
    }

    const editor = originalInitQuillEditor(editorId, contentInputId, formId, initialContent);
    window.initedEditors[editorId] = editor;
    return editor;
};


