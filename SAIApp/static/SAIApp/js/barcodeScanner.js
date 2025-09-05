const btnCloseScanner = document.getElementById("btn_close_scanner");
const btnTorch = document.getElementById("btn_torch");

let fieldToFill = null;
let capabilities = null;
let cameraId = localStorage.getItem("selectedCameraId") || null;
let qrboxWidth = 400;
let html5QrCode = null;
let torchFeature = null;

btnCloseScanner.onclick = () => stopScanning();
btnTorch.onclick = () => toggleTorch();

if (navigator.userAgentData?.mobile) {
    qrboxWidth = 250;
}

console.log(qrboxWidth);

let config = {
    qrbox: qrboxWidth,
    fps: 20
};

if(!cameraId){
    Html5Qrcode.getCameras().then(devices => {
        if (devices && devices.length) {
            cameraId = devices.find(device => device.label.includes("back"))?.id || devices[0].id;
            console.log("Selected camera:", cameraId);

            localStorage.setItem("selectedCameraId", cameraId);

            html5QrCode = new Html5Qrcode("reader");
        }
    }).catch(err => {
        console.error("Error getting cameras:", err);
    });
} else {
    html5QrCode = new Html5Qrcode("reader");

}


function qrCodeSuccessCallback(decodedText, decodedResult) {
    console.log("QR Code detected:", decodedText);
    fieldToFill.value = decodedText;
    stopScanning();
}

function qrCodeErrorCallback(error) {
    console.warn("QR Code scan error:", error);
}

async function startScanning() {
    if (!html5QrCode) {
        console.error("QR Scanner not initialized yet.");
        return;
    }

    console.log("Starting scan with camera ID:", cameraId);

    try {
        await html5QrCode.start(cameraId, config, qrCodeSuccessCallback, qrCodeErrorCallback);

        capabilities = await html5QrCode.getRunningTrackCameraCapabilities();
        if (capabilities && capabilities.torchFeature().isSupported()) {
            torchFeature = capabilities.torchFeature();
            btnTorch.disabled = false;
        }
    } catch (err) {
        console.error("Failed to start scanning:", err);
    }
}

async function stopScanning() {
    if (html5QrCode) {
        try {
            await html5QrCode.stop();
            console.log("Scanning stopped.");
            btnTorch.classList.remove("active");
            btnCloseScanner.click();
        } catch (err) {
            console.error("Failed to stop scanning:", err);
        }
    }
}

function toggleTorch() {
    if (torchFeature) {
        torchFeature.apply(!torchFeature.value());
        btnTorch.classList.toggle("active");
    } else {
        console.log("Torch feature not available.");
    }
}

