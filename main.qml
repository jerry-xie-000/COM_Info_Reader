import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14

ApplicationWindow {
    visible: true
    width: 720
    height: 560
    title: "凯捷信息读取工具"
    font.pixelSize: 26

    ColumnLayout{
        anchors.fill: parent

        spacing: 20

        GridLayout{
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            columns: 2
            columnSpacing: 30
            rowSpacing: 30
            Label{
                text:qsTr("型号")
            }

            Label{
                text:qsTr("???")
                objectName: "lblType"
            }

            Label{
                text:qsTr("MAC")
            }

            Label{
                text:qsTr("???")
                objectName: "lblMAC"
            }

            Label{
                text:qsTr("序列号")
            }

            Label{
                text:qsTr("???")
                objectName: "lblNo"
            }
        }

        RowLayout{
            Layout.rowSpan: 19
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Label{
                text:qsTr("串口")
            }

            ComboBox{
                Layout.preferredWidth: 500
                objectName: "cmbPort"
            }

            Button{
                objectName: "btnOpen"

                text:qsTr("打开")
                onClicked: Ser.on_btnOpen_clicked()

            }
        }

        Label{
            objectName: "lblTip"
			Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        Button{
            text:qsTr("读取")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: Ser.on_btnRead_clicked()

        }
    }



    onClosing: {
        Ser.on_closed()
    }
}
