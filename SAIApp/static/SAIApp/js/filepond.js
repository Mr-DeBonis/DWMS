function createFilepondElement() {
    FilePond.registerPlugin(
        FilePondPluginFileValidateType,
        FilePondPluginImagePreview,
        FilePondPluginImageResize,
        FilePondPluginImageTransform,
    );

    FilePond.setOptions({
        // Core
        allowMultiple: true,
        maxFiles: 3,
        credits: false,
        // Drag n' Drop
        dropOnPage: true,
        dropOnElement: true,
        dropValidation: true,
        // Server
        server: null,
        // Labels
        labelIdle: '<span class="filepond--label-action"><span class="glyphicon glyphicon-camera" aria-hidden="true"></span> Suba sus fotos </span>',
        labelInvalidField: 'Archivos inválidos',
        labelFileWaitingForSize: 'Calculando tamaño de archivo',
        labelFileSizeNotAvailable: 'Tamaño no disponible',
        labelFileLoading: 'Cargando',
        labelFileLoadError: 'Error al cargar archivo',
        labelFileProcessing: 'Cargando archivo',
        labelFileProcessingComplete: 'Carga completada',
        labelFileProcessingAborted: 'Carga cancelada',
        labelFileProcessingError: 'Error al cargar archivo',
        labelFileProcessingRevertError: 'Error durante la devolución',
        labelFileRemoveError: 'Error al remover archivo',
        labelTapToCancel: 'Presione para cancelar',
        labelTapToRetry: 'Presione para reintentar',
        labelTapToUndo: 'Presione para deshacer',
        labelButtonRemoveItem: 'Remover',
        labelButtonAbortItemLoad: 'Cancelar',
        labelButtonRetryItemLoad: 'Reintentar',
        labelButtonAbortItemProcessing: 'Cancelar',
        labelButtonUndoItemProcessing: 'Deshacer',
        labelButtonRetryItemProcessing: 'Reintentar',
        labelButtonProcessItem: 'Cargar',
    });

    const inputElement = document.getElementById('filepond');//querySelector('input[type="file"]');
    return pond = FilePond.create(inputElement, {
        acceptedFileTypes: ['image/*'],
        labelFileTypeNotAllowed: 'Formato de archivo inválido. Ingrese fotos o imágenes.',
        // Resize before upload
        imageResizeTargetWidth: 1280,
        imageResizeTargetHeight: 1280,
        imageResizeMode: 'contain',
        imageResizeUpscale: "false",
        // Compression
        //allowImageTransform: true,
        //imageTransformVariantsIncludeDefault: false,
        //imageTransformOutputQuality: 90,
        imageTransformOutputMimeType: 'image/jpeg', // force to JPEG
        onremovefile: (err, file) => {
            transformedFilesMap.delete(file.id);
        },
        onpreparefile: (file, output) => {
            const outputFile = new File([output], output.name, {type: output.type});
            transformedFilesMap.set(file.id, outputFile);
        }
    });
}

