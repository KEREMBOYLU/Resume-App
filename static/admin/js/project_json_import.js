(function () {
  'use strict';

  const SAMPLE_JSON = JSON.stringify({
    title: 'Example Project',
    slug: 'example-project',
    category: 'iOS Development',
    status: 'in_progress',
    summary: 'Short project summary shown in cards and the project hero.',
    tech_stack: ['Swift', 'SwiftUI', 'CloudKit'],
    is_featured: true,
    order: 1,
    links: [
      {
        label: 'GitHub',
        url: 'https://github.com/example/project',
        icon: '<i class="fa-brands fa-github"></i>',
        is_primary: true,
        order: 0
      }
    ],
    sections: [
      {
        type: 'overview',
        title: 'Project Overview',
        content: '<p>Project overview content.</p>',
        order: 0
      },
      {
        type: 'features',
        title: 'Key Features',
        items: ['First feature', 'Second feature'],
        order: 1
      },
      {
        type: 'timeline',
        title: 'Project Timeline',
        items: [
          {
            date: '01.01.2026',
            title: 'Kickoff',
            description: 'Started the project.'
          }
        ],
        order: 2
      }
    ]
  }, null, 2);

  const SECTION_TYPE_MAP = {
    overview: 'custom_html',
    technical: 'custom_html',
    architecture: 'custom_html',
    learning: 'custom_html',
    custom: 'custom_html',
    custom_html: 'custom_html',
    features: 'feature_list',
    feature_list: 'feature_list',
    timeline: 'timeline',
    gallery: 'gallery'
  };

  function ready(callback) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', callback);
      return;
    }
    callback();
  }

  function getField(name) {
    return document.getElementById(`id_${name}`) || document.querySelector(`[name="${name}"]`);
  }

  function setField(name, value) {
    const field = getField(name);
    if (!field || value === undefined || value === null) {
      return;
    }

    if (field.type === 'checkbox') {
      field.checked = Boolean(value);
    } else {
      field.value = String(value);
    }

    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function setSelectByTextOrValue(name, value) {
    const field = getField(name);
    if (!field || value === undefined || value === null) {
      return;
    }

    const normalized = String(value).trim().toLowerCase();
    const option = Array.from(field.options).find((item) => (
      item.value === String(value) ||
      item.textContent.trim().toLowerCase() === normalized
    ));

    if (option) {
      field.value = option.value;
      field.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  function normalizeTechStack(value) {
    if (Array.isArray(value)) {
      return value.filter(Boolean).join(', ');
    }
    return value || '';
  }

  function normalizeFeatureItems(section) {
    const items = section.items || section.features || section.data;
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((item) => {
      if (typeof item === 'string') {
        return { title: item };
      }
      return item;
    });
  }

  function normalizeTimelineItems(section) {
    const items = section.items || section.timeline || section.data;
    return Array.isArray(items) ? items : [];
  }

  function normalizeSectionType(type) {
    return SECTION_TYPE_MAP[String(type || '').trim().toLowerCase()] || 'custom_html';
  }

  function getInlineRows(prefix) {
    return Array.from(document.querySelectorAll(`#${prefix}-group [id^="${prefix}-"]`)).filter((row) => (
      row.id !== `${prefix}-empty` &&
      /^\w/.test(row.id) &&
      new RegExp(`^${prefix}-\\d+$`).test(row.id) &&
      !row.classList.contains('empty-form') &&
      !row.querySelector(`[name$="-DELETE"]`)?.checked
    ));
  }

  function resolveInlinePrefix(candidates) {
    return candidates.find((prefix) => (
      document.getElementById(`${prefix}-group`) ||
      document.getElementById(`id_${prefix}-TOTAL_FORMS`)
    ));
  }

  function addInlineRow(prefix) {
    const addLink = document.querySelector(`#${prefix}-group .add-row a`);
    if (!addLink) {
      return null;
    }

    addLink.click();
    const rows = getInlineRows(prefix);
    return rows[rows.length - 1] || null;
  }

  function ensureInlineRows(prefix, count) {
    let rows = getInlineRows(prefix);
    while (rows.length < count) {
      const row = addInlineRow(prefix);
      if (!row) {
        break;
      }
      rows = getInlineRows(prefix);
    }
    return rows;
  }

  function setInlineField(row, fieldName, value) {
    if (!row || value === undefined || value === null) {
      return;
    }

    const field = row.querySelector(`[name$="-${fieldName}"]`);
    if (!field) {
      return;
    }

    if (field.type === 'checkbox') {
      field.checked = Boolean(value);
    } else if (field.tagName === 'TEXTAREA' && typeof value !== 'string') {
      field.value = JSON.stringify(value, null, 2);
    } else {
      field.value = String(value);
    }

    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function fillLinks(project) {
    const links = Array.isArray(project.links) ? project.links.slice() : [];

    if (project.github_url && !links.some((link) => link.url === project.github_url)) {
      links.push({
        label: 'GitHub',
        url: project.github_url,
        icon: '<i class="fa-brands fa-github"></i>',
        is_primary: !links.length,
        order: links.length
      });
    }

    if (!links.length) {
      return;
    }

    const prefix = resolveInlinePrefix(['hero_links', 'projectlink_set']);
    if (!prefix) {
      return;
    }

    const rows = ensureInlineRows(prefix, links.length);
    links.forEach((link, index) => {
      const row = rows[index];
      setInlineField(row, 'label', link.label);
      setInlineField(row, 'url', link.url);
      setInlineField(row, 'icon', link.icon || '');
      setInlineField(row, 'is_primary', Boolean(link.is_primary));
      setInlineField(row, 'order', link.order ?? index);
    });
  }

  function fillSections(project) {
    const sections = Array.isArray(project.sections) ? project.sections : [];
    if (!sections.length) {
      return;
    }

    const prefix = resolveInlinePrefix(['sections', 'projectsection_set']);
    if (!prefix) {
      return;
    }

    const rows = ensureInlineRows(prefix, sections.length);
    sections.forEach((section, index) => {
      const row = rows[index];
      const sectionType = normalizeSectionType(section.type || section.section_type);

      let data = section.data || {};
      if (sectionType === 'feature_list') {
        data = { features: normalizeFeatureItems(section) };
      } else if (sectionType === 'timeline') {
        data = { items: normalizeTimelineItems(section) };
      }

      setInlineField(row, 'section_type', sectionType);
      setInlineField(row, 'title', section.title || '');
      setInlineField(row, 'order', section.order ?? index);
      setInlineField(row, 'is_active', section.is_active ?? true);
      setInlineField(row, 'content', section.content || section.description || '');
      setInlineField(row, 'data', data);
    });
  }

  function fillProject(project) {
    setField('title', project.title);
    setField('slug', project.slug);
    setField('summary', project.summary || project.description);
    setField('status', project.status);
    setField('tech_stack', normalizeTechStack(project.tech_stack || project.technologies));
    setField('is_featured', project.is_featured);
    setField('order', project.order);
    setSelectByTextOrValue('category', project.category || project.category_id);

    fillLinks(project);
    fillSections(project);
  }

  function buildModal() {
    const wrapper = document.createElement('div');
    wrapper.id = 'project-json-import-modal';
    wrapper.style.cssText = [
      'display:none',
      'position:fixed',
      'inset:0',
      'z-index:10000',
      'background:rgba(0,0,0,0.55)',
      'align-items:center',
      'justify-content:center',
      'padding:24px'
    ].join(';');

    wrapper.innerHTML = `
      <div style="width:min(960px, 100%); max-height:90vh; overflow:auto; background:var(--body-bg, #fff); color:var(--body-fg, #111); border-radius:10px; box-shadow:0 20px 70px rgba(0,0,0,.35);">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 18px; border-bottom:1px solid var(--hairline-color, #ddd);">
          <h2 style="margin:0; font-size:18px;">Import Project JSON</h2>
          <button type="button" data-json-import-close class="button">Close</button>
        </div>
        <div style="padding:18px;">
          <p style="margin:0 0 12px; color:var(--body-quiet-color, #666);">
            Paste project JSON here. Image fields are intentionally ignored.
          </p>
          <textarea data-json-import-input spellcheck="false" style="box-sizing:border-box; width:100%; min-height:420px; font-family:monospace; font-size:13px;"></textarea>
          <p data-json-import-error style="display:none; margin:12px 0 0; color:#ba2121; font-weight:600;"></p>
        </div>
        <div style="display:flex; justify-content:flex-end; gap:10px; padding:14px 18px; border-top:1px solid var(--hairline-color, #ddd);">
          <button type="button" data-json-import-sample class="button">Insert sample</button>
          <button type="button" data-json-import-submit class="default">Fill form</button>
        </div>
      </div>
    `;

    document.body.appendChild(wrapper);
    return wrapper;
  }

  function init() {
    if (!document.body.classList.contains('app-projects') || !document.body.classList.contains('model-project')) {
      return;
    }

    const modal = buildModal();
    const textarea = modal.querySelector('[data-json-import-input]');
    const error = modal.querySelector('[data-json-import-error]');

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'button';
    button.textContent = 'Import JSON';
    button.style.marginLeft = '8px';

    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
      submitRow.prepend(button);
    }

    const open = () => {
      error.style.display = 'none';
      error.textContent = '';
      modal.style.display = 'flex';
      textarea.focus();
    };

    const close = () => {
      modal.style.display = 'none';
    };

    button.addEventListener('click', open);
    modal.querySelector('[data-json-import-close]').addEventListener('click', close);
    modal.querySelector('[data-json-import-sample]').addEventListener('click', () => {
      textarea.value = SAMPLE_JSON;
      textarea.focus();
    });
    modal.addEventListener('click', (event) => {
      if (event.target === modal) {
        close();
      }
    });

    modal.querySelector('[data-json-import-submit]').addEventListener('click', () => {
      try {
        const project = JSON.parse(textarea.value);
        fillProject(project);
        close();
      } catch (exception) {
        error.textContent = `Invalid JSON: ${exception.message}`;
        error.style.display = 'block';
      }
    });
  }

  ready(init);
}());
