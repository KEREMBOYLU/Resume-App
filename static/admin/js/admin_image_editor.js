(function () {
    const editorState = new WeakMap();

    function initEditors(root) {
        const scope = root || document;
        scope.querySelectorAll('[data-admin-image-editor]').forEach((wrapper) => {
            if (wrapper.dataset.editorReady === '1') {
                return;
            }
            wrapper.dataset.editorReady = '1';
            setupEditor(wrapper);
        });
    }

    function setupEditor(wrapper) {
        const input = wrapper.querySelector('input[type="file"]');
        const emptyPreview = wrapper.querySelector('[data-editor-empty-preview]');
        const openButton = wrapper.querySelector('[data-editor-open]');
        const modal = wrapper.querySelector('[data-editor-modal]');
        const image = wrapper.querySelector('[data-editor-image]');
        const confirmButton = wrapper.querySelector('[data-editor-confirm]');
        const hint = wrapper.querySelector('[data-editor-hint]');
        const pasteButton = wrapper.querySelector('[data-editor-paste]');
        const pasteHint = wrapper.querySelector('[data-editor-paste-hint]');
        const customWidthInput = wrapper.querySelector('[data-editor-custom-width]');
        const customHeightInput = wrapper.querySelector('[data-editor-custom-height]');
        const zoomRange = wrapper.querySelector('[data-editor-zoom-range]');
        const state = {
            cropper: null,
            objectUrl: null,
            canConfirm: false,
            fileName: 'cropped-image.jpg',
            mimeType: 'image/jpeg',
            outputWidth: null,
            outputHeight: null,
        };
        editorState.set(wrapper, state);

        if (!input || !modal || !image) {
            return;
        }

        input.addEventListener('change', () => {
            const file = input.files && input.files[0];
            if (!file) {
                return;
            }
            openFileInEditor(file);
        });

        wrapper.addEventListener('paste', (event) => {
            const file = getClipboardImageFile(event.clipboardData);
            if (!file) {
                showPasteMessage('Clipboard does not contain an image.');
                return;
            }
            event.preventDefault();
            openFileInEditor(file);
        });

        if (pasteButton) {
            pasteButton.addEventListener('click', () => pasteImageFromClipboard());
        }

        if (openButton) {
            openButton.addEventListener('click', () => {
                const previewImage = wrapper.querySelector('[data-editor-preview]');
                const src = previewImage ? previewImage.getAttribute('src') : '';
                if (src) {
                    openEditor(wrapper, src, false);
                }
            });
        }

        wrapper.querySelectorAll('[data-editor-close]').forEach((button) => {
            button.addEventListener('click', () => closeEditor(wrapper));
        });

        wrapper.querySelectorAll('[data-editor-ratio]').forEach((button) => {
            button.addEventListener('click', () => {
                const currentState = editorState.get(wrapper);
                const cropper = currentState.cropper;
                if (!cropper) {
                    return;
                }
                const ratio = Number(button.dataset.editorRatio);
                currentState.outputWidth = null;
                currentState.outputHeight = null;
                clearCustomSize();
                cropper.setAspectRatio(Number.isNaN(ratio) ? NaN : ratio);
                setActivePreset(button);
            });
        });

        wrapper.querySelectorAll('[data-editor-mode]').forEach((button) => {
            button.addEventListener('click', () => {
                const cropper = editorState.get(wrapper).cropper;
                if (cropper) {
                    cropper.setDragMode(button.dataset.editorMode);
                }
            });
        });

        wrapper.querySelectorAll('[data-editor-zoom]').forEach((button) => {
            button.addEventListener('click', () => {
                const cropper = editorState.get(wrapper).cropper;
                if (cropper) {
                    cropper.zoom(Number(button.dataset.editorZoom));
                    syncZoomRange(wrapper);
                }
            });
        });

        if (zoomRange) {
            zoomRange.addEventListener('input', () => {
                const cropper = editorState.get(wrapper).cropper;
                if (cropper) {
                    cropper.zoomTo(Number(zoomRange.value));
                }
            });
        }

        wrapper.querySelectorAll('[data-editor-rotate]').forEach((button) => {
            button.addEventListener('click', () => {
                const cropper = editorState.get(wrapper).cropper;
                if (cropper) {
                    cropper.rotate(Number(button.dataset.editorRotate));
                }
            });
        });

        const resetButton = wrapper.querySelector('[data-editor-reset]');
        if (resetButton) {
            resetButton.addEventListener('click', () => {
                const currentState = editorState.get(wrapper);
                const cropper = currentState.cropper;
                if (cropper) {
                    cropper.reset();
                    currentState.outputWidth = null;
                    currentState.outputHeight = null;
                    clearCustomSize();
                    clearActivePresets();
                    resetZoomRange();
                }
            });
        }

        const applySizeButton = wrapper.querySelector('[data-editor-apply-size]');
        if (applySizeButton) {
            applySizeButton.addEventListener('click', () => applyCustomSize(wrapper));
        }

        const clearSizeButton = wrapper.querySelector('[data-editor-clear-size]');
        if (clearSizeButton) {
            clearSizeButton.addEventListener('click', () => {
                const currentState = editorState.get(wrapper);
                currentState.outputWidth = null;
                currentState.outputHeight = null;
                clearCustomSize();
                clearActivePresets();
                if (currentState.cropper) {
                    currentState.cropper.setAspectRatio(NaN);
                }
            });
        }

        if (confirmButton) {
            confirmButton.addEventListener('click', () => confirmCrop(wrapper));
        }

        function openFileInEditor(file) {
            state.fileName = file.name || `pasted-image.${extensionForMimeType(file.type)}`;
            state.mimeType = file.type || 'image/png';
            openEditor(wrapper, URL.createObjectURL(file), true);
            showPasteMessage('Image loaded. Crop it and confirm before saving.');
        }

        async function pasteImageFromClipboard() {
            if (!navigator.clipboard || !navigator.clipboard.read) {
                showPasteMessage('Use Cmd/Ctrl+V after clicking this image field.');
                wrapper.focus();
                return;
            }

            try {
                const clipboardItems = await navigator.clipboard.read();
                const file = await getImageFileFromClipboardItems(clipboardItems);
                if (!file) {
                    showPasteMessage('Clipboard does not contain an image.');
                    return;
                }
                openFileInEditor(file);
            } catch (error) {
                showPasteMessage('Clipboard access was blocked. Click the field and press Cmd/Ctrl+V.');
                wrapper.focus();
            }
        }

        function openEditor(wrapper, src, canConfirm) {
            const currentState = editorState.get(wrapper);
            destroyCropper(currentState);
            currentState.canConfirm = canConfirm;
            currentState.outputWidth = null;
            currentState.outputHeight = null;
            clearCustomSize();
            clearActivePresets();
            resetZoomRange();
            if (canConfirm && src.startsWith('blob:')) {
                currentState.objectUrl = src;
            }

            image.onload = () => {
                if (!window.Cropper) {
                    if (hint) {
                        hint.textContent = 'Resim düzenleyici yüklenemedi.';
                    }
                    return;
                }
                currentState.cropper = new window.Cropper(image, {
                    viewMode: 1,
                    dragMode: 'move',
                    autoCropArea: 0.9,
                    background: false,
                    responsive: true,
                    checkOrientation: true,
                    crop() {
                        syncZoomRange(wrapper);
                    },
                });
            };

            image.src = src;
            modal.hidden = false;
            document.body.classList.add('admin-image-editor-open');

            if (confirmButton) {
                confirmButton.disabled = !canConfirm;
            }
            if (hint) {
                hint.textContent = canConfirm
                    ? 'Resmi düzenle, sonra kaydetmeden önce kırpmayı onayla.'
                    : 'Mevcut resim önizlemesi. Değiştirmek için yeni dosya seç.';
            }
        }

        function closeEditor(wrapper) {
            const currentState = editorState.get(wrapper);
            destroyCropper(currentState);
            modal.hidden = true;
            image.removeAttribute('src');
            document.body.classList.remove('admin-image-editor-open');
        }

        function confirmCrop(wrapper) {
            const currentState = editorState.get(wrapper);
            if (!currentState.cropper || !currentState.canConfirm) {
                return;
            }

            const canvasOptions = {
                imageSmoothingEnabled: true,
                imageSmoothingQuality: 'high',
            };
            if (currentState.outputWidth && currentState.outputHeight) {
                canvasOptions.width = currentState.outputWidth;
                canvasOptions.height = currentState.outputHeight;
            }

            const canvas = currentState.cropper.getCroppedCanvas(canvasOptions);

            if (!canvas) {
                return;
            }

            canvas.toBlob((blob) => {
                if (!blob) {
                    return;
                }

                const file = new File([blob], currentState.fileName, {
                    type: currentState.mimeType,
                    lastModified: Date.now(),
                });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                input.files = dataTransfer.files;

                const previewUrl = URL.createObjectURL(blob);
                updatePreview(previewUrl);
                uncheckClearBox(input);
                closeEditor(wrapper);
            }, currentState.mimeType);
        }

        function updatePreview(src) {
            let previewImage = wrapper.querySelector('[data-editor-preview]');
            if (!previewImage) {
                previewImage = document.createElement('img');
                previewImage.alt = '';
                previewImage.className = 'admin-image-editor__preview';
                previewImage.dataset.editorPreview = '';
                wrapper.querySelector('.admin-image-editor__preview-wrap').replaceChildren(previewImage);
            }
            previewImage.src = src;
            if (emptyPreview) {
                emptyPreview.hidden = true;
            }
            if (openButton) {
                openButton.hidden = false;
            }
        }

        function applyCustomSize(wrapper) {
            const currentState = editorState.get(wrapper);
            const cropper = currentState.cropper;
            const width = Number(customWidthInput && customWidthInput.value);
            const height = Number(customHeightInput && customHeightInput.value);
            if (!cropper || !Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
                if (hint) {
                    hint.textContent = 'Geçerli bir genişlik ve yükseklik gir.';
                }
                return;
            }

            currentState.outputWidth = Math.round(width);
            currentState.outputHeight = Math.round(height);
            cropper.setAspectRatio(width / height);
            clearActivePresets();
            if (hint) {
                hint.textContent = `Çıktı ölçüsü ${currentState.outputWidth} x ${currentState.outputHeight}px olarak ayarlandı.`;
            }
        }

        function clearCustomSize() {
            if (customWidthInput) {
                customWidthInput.value = '';
            }
            if (customHeightInput) {
                customHeightInput.value = '';
            }
        }

        function setActivePreset(activeButton) {
            wrapper.querySelectorAll('[data-editor-preset]').forEach((button) => {
                button.classList.toggle('admin-image-editor__preset--active', button === activeButton);
            });
        }

        function clearActivePresets() {
            wrapper.querySelectorAll('[data-editor-preset]').forEach((button) => {
                button.classList.remove('admin-image-editor__preset--active');
            });
        }

        function resetZoomRange() {
            if (zoomRange) {
                zoomRange.value = '1';
            }
        }

        function showPasteMessage(message) {
            if (pasteHint) {
                pasteHint.textContent = message;
            }
        }
    }

    function getClipboardImageFile(clipboardData) {
        if (!clipboardData || !clipboardData.items) {
            return null;
        }

        for (const item of clipboardData.items) {
            if (item.kind === 'file' && item.type && item.type.startsWith('image/')) {
                const file = item.getAsFile();
                return ensureImageFileName(file);
            }
        }

        return null;
    }

    async function getImageFileFromClipboardItems(clipboardItems) {
        for (const item of clipboardItems) {
            const imageType = item.types.find((type) => type.startsWith('image/'));
            if (!imageType) {
                continue;
            }
            const blob = await item.getType(imageType);
            return ensureImageFileName(blob);
        }
        return null;
    }

    function ensureImageFileName(fileOrBlob) {
        if (!fileOrBlob) {
            return null;
        }
        if (fileOrBlob instanceof File && fileOrBlob.name) {
            return fileOrBlob;
        }
        const type = fileOrBlob.type || 'image/png';
        return new File([fileOrBlob], `pasted-image.${extensionForMimeType(type)}`, {
            type,
            lastModified: Date.now(),
        });
    }

    function extensionForMimeType(mimeType) {
        const type = mimeType || 'image/png';
        if (type.includes('jpeg') || type.includes('jpg')) {
            return 'jpg';
        }
        if (type.includes('webp')) {
            return 'webp';
        }
        if (type.includes('gif')) {
            return 'gif';
        }
        return 'png';
    }

    function syncZoomRange(wrapper) {
        const state = editorState.get(wrapper);
        const zoomRange = wrapper.querySelector('[data-editor-zoom-range]');
        if (!state || !state.cropper || !zoomRange) {
            return;
        }
        const imageData = state.cropper.getImageData();
        if (!imageData || !imageData.naturalWidth) {
            return;
        }
        const zoom = imageData.width / imageData.naturalWidth;
        const min = Number(zoomRange.min);
        const max = Number(zoomRange.max);
        zoomRange.value = String(Math.min(max, Math.max(min, zoom)));
    }

    function destroyCropper(state) {
        if (state && state.cropper) {
            state.cropper.destroy();
            state.cropper = null;
        }
        if (state && state.objectUrl) {
            URL.revokeObjectURL(state.objectUrl);
            state.objectUrl = null;
        }
    }

    function uncheckClearBox(input) {
        const clearBox = document.querySelector(`input[type="checkbox"][name="${input.name}-clear"]`);
        if (clearBox) {
            clearBox.checked = false;
        }
    }

    document.addEventListener('DOMContentLoaded', () => initEditors(document));
    document.addEventListener('formset:added', (event) => initEditors(event.target));
})();
