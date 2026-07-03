Attribute VB_Name = "Module2"
Option Explicit

Public Sub Run_Consolidation()

    Dim startTime As Double
    startTime = Timer   ' ? start timer

    Application.ScreenUpdating = False
    Application.EnableEvents = False
    Application.DisplayAlerts = False
    Application.Calculation = xlCalculationManual

    Dim schema As Object, schemaIsDate As Object
    Set schema = LoadSchema(schemaIsDate)

    Dim datasets As Object
    Set datasets = LoadDatasets()

    Dim mappings As Object
    Set mappings = LoadMappings()

    Dim files As Object
    Set files = PickInputFiles(datasets)   ' ? fixed prompt name here

    Dim outWB As Workbook, outWS As Worksheet
    Set outWB = Workbooks.Add(xlWBATWorksheet)
    Set outWS = outWB.sheets(1)
    outWS.name = "Consolidated"

    WriteHeaders outWS, schema

    Dim logWS As Worksheet
    Set logWS = PrepareMissingSheetLog(outWB)

    Dim nextRow As Long: nextRow = 2
    Dim logRow As Long: logRow = 2

    ProcessAll datasets, mappings, schema, schemaIsDate, files, outWS, nextRow, logWS, logRow

    Dim outPath As String
    outPath = PickOutputFolder() & "\Consolidated_Output.xlsx"
    outWB.SaveAs outPath, xlOpenXMLWorkbook

    Application.ScreenUpdating = True
    Application.EnableEvents = True
    Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic

    ' ? calculate elapsed time
    Dim elapsed As Double
    elapsed = Timer - startTime

    MsgBox "Consolidation completed successfully." & vbCrLf & _
           "Time taken: " & _
           Int(elapsed / 60) & " min " & _
           Format(elapsed Mod 60, "0.00") & " sec", _
           vbInformation

End Sub

'================ SCHEMA =================

Private Function LoadSchema(ByRef isDate As Object) As Object
    Dim d As Object: Set d = CreateObject("Scripting.Dictionary")
    Set isDate = CreateObject("Scripting.Dictionary")

    Dim ws As Worksheet: Set ws = ThisWorkbook.sheets("Schema_Config")
    Dim r As Long: r = 2

    Do While ws.Cells(r, 1).Value <> ""
        d(CLng(ws.Cells(r, 1).Value)) = ws.Cells(r, 2).Value
        isDate(ws.Cells(r, 2).Value) = (UCase(ws.Cells(r, 3).Value) = "Y")
        r = r + 1
    Loop

    Set LoadSchema = d
End Function

Private Sub WriteHeaders(ws As Worksheet, schema As Object)
    Dim k As Variant
    For Each k In schema.Keys
        ws.Cells(1, k).Value = schema(k)
        ws.Cells(1, k).Interior.Color = RGB(131, 226, 142)
    Next
End Sub

'================ DATASETS =================

Private Function LoadDatasets() As Object

    Dim d As Object
    Set d = CreateObject("Scripting.Dictionary")

    Dim ws As Worksheet
    Set ws = ThisWorkbook.sheets("Dataset_Config")

    Dim r As Long
    r = 2

    Do While ws.Cells(r, 1).Value <> ""

        d(ws.Cells(r, 2).Value & "|" & ws.Cells(r, 4).Value) = Array( _
            ws.Cells(r, 3).Value, _
            ws.Cells(r, 5).Value, _
            ws.Cells(r, 2).Value, _
            ws.Cells(r, 6).Value _
        )

        r = r + 1
    Loop

    Set LoadDatasets = d

End Function


'================ MAPPINGS =================

Private Function LoadMappings() As Object
    Dim d As Object: Set d = CreateObject("Scripting.Dictionary")
    Dim ws As Worksheet: Set ws = ThisWorkbook.sheets("Mapping_Config")
    Dim r As Long: r = 2

    Do While ws.Cells(r, 1).Value <> ""
        Dim key As String
        key = ws.Cells(r, 1).Value & "|" & ws.Cells(r, 2).Value
        If Not d.Exists(key) Then Set d(key) = CreateObject("Scripting.Dictionary")
        d(key)(ws.Cells(r, 4).Value) = ws.Cells(r, 3).Value
        r = r + 1
    Loop

    Set LoadMappings = d
End Function

'================ FILE PICKER =================

Private Function PickInputFiles(datasets As Object) As Object

    Dim files As Object: Set files = CreateObject("Scripting.Dictionary")
    Dim prompted As Object: Set prompted = CreateObject("Scripting.Dictionary")

    Dim k As Variant
    For Each k In datasets.Keys

        Dim fg As String: fg = datasets(k)(0)
        Dim promptName As String: promptName = datasets(k)(3)  ' ? correct column

        If Not prompted.Exists(fg) Then

            Dim f As Variant
            f = Application.GetOpenFilename( _
                    "Excel Files (*.xlsx),*.xlsx", , _
                    "Select input file: " & promptName)

            If f = False Then Err.Raise 9999, , "File selection cancelled."

            files(fg) = f
            prompted(fg) = True
        End If
    Next

    Set PickInputFiles = files
End Function

Private Function PickOutputFolder() As String
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Show
        PickOutputFolder = .SelectedItems(1)
    End With
End Function

'================ PROCESS =================

Private Sub ProcessAll(datasets As Object, mappings As Object, schema As Object, isDate As Object, _
                       files As Object, outWS As Worksheet, ByRef nextRow As Long, _
                       logWS As Worksheet, ByRef logRow As Long)

    Dim dsKey As Variant
    For Each dsKey In datasets.Keys

        Dim parts() As String: parts = Split(dsKey, "|")
        Dim dataset As String: dataset = parts(0)
        Dim sheetName As String: sheetName = parts(1)

        Dim fg As String: fg = datasets(dsKey)(0)
        Dim tableVal As String: tableVal = datasets(dsKey)(1)

        Dim wb As Workbook: Set wb = Workbooks.Open(files(fg), False, True)

        Dim ws As Worksheet
        Set ws = Nothing
        On Error Resume Next
        Set ws = wb.Worksheets(sheetName)
        On Error GoTo 0

        If ws Is Nothing Then
            logWS.Cells(logRow, 1).Value = dataset
            logWS.Cells(logRow, 2).Value = sheetName
            logWS.Cells(logRow, 3).Value = wb.name
            logRow = logRow + 1
            wb.Close False
            GoTo NextDataset
        End If

        Dim hdrRow As Long: hdrRow = DetectHeaderRow(ws)
        Dim hdrPos As Object: Set hdrPos = MapHeaders(ws, hdrRow)
        Dim lastRow As Long: lastRow = ws.Cells(ws.rows.Count, 1).End(xlUp).Row

        Dim r As Long
        For r = hdrRow + 1 To lastRow

            Dim outCol As Variant
            For Each outCol In schema.Keys

                Dim tgt As String: tgt = schema(outCol)
                Dim val As String: val = ""

                If tgt = "Table" Then
                    val = tableVal
                ElseIf mappings.Exists(dataset & "|" & sheetName) Then
                    If mappings(dataset & "|" & sheetName).Exists(tgt) Then
                        Dim src As String: src = mappings(dataset & "|" & sheetName)(tgt)
                        If hdrPos.Exists(src) Then
                            If Not IsError(ws.Cells(r, hdrPos(src)).Value) Then
                                val = Trim(CStr(ws.Cells(r, hdrPos(src)).Value))
                            End If
                        End If
                    End If
                End If

                If val = "" And Not isDate(tgt) Then val = "Not Defined"
                outWS.Cells(nextRow, outCol).Value = val

            Next outCol
            nextRow = nextRow + 1
        Next r

        wb.Close False

NextDataset:
    Next dsKey

End Sub

'================ LOG =================

Private Function PrepareMissingSheetLog(wb As Workbook) As Worksheet
    Dim ws As Worksheet
    Set ws = wb.sheets.Add(After:=wb.sheets(wb.sheets.Count))
    ws.name = "Missing_Sheets_Log"
    ws.Cells(1, 1).Value = "Dataset"
    ws.Cells(1, 2).Value = "SheetName"
    ws.Cells(1, 3).Value = "Workbook"
    ws.rows(1).Font.Bold = True
    Set PrepareMissingSheetLog = ws
End Function

'================ HELPERS =================

Private Function DetectHeaderRow(ws As Worksheet) As Long
    Dim r As Long, c As Long
    For r = 1 To 50
        For c = 1 To 50
            If Not IsError(ws.Cells(r, c).Value) Then
                If Trim(CStr(ws.Cells(r, c).Value)) <> "" Then
                    DetectHeaderRow = r
                    Exit Function
                End If
            End If
        Next c
    Next r
    Err.Raise 9999, , "Header row not detected"
End Function

Private Function MapHeaders(ws As Worksheet, hdrRow As Long) As Object
    Dim d As Object: Set d = CreateObject("Scripting.Dictionary")
    Dim c As Long
    For c = 1 To ws.Cells(hdrRow, ws.Columns.Count).End(xlToLeft).Column
        If Not IsError(ws.Cells(hdrRow, c).Value) Then
            d(Trim(CStr(ws.Cells(hdrRow, c).Value))) = c
        End If
    Next c
    Set MapHeaders = d
End Function


