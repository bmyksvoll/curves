Option Explicit
Option Base 1

Const NUMCOEFF = 5
Const APOS = 1, BPOS = 2, CPOS = 3, DPOS = 4, EPOS = 5


Public Function comp(rngTradedate As Variant, rngInPeriods As Variant, _
                    rngInPrices As Variant, rngOutPeriods, _
                    Optional rngIncludeFlag As Variant) As Variant

Dim tradedate As Date, InPeriods As Variant, InPrices As Variant
Dim IncludeFlag As Variant, IncludePeriods As Variant, IncludePrices As Variant
Dim Outperiods As Variant
Dim i As Long, iCount As Long


    InPeriods = rngInPeriods.Value
    InPrices = rngInPrices.Value
    tradedate = rngTradedate.Value
    Outperiods = rngOutPeriods.Value
    
    If Not IsMissing(rngIncludeFlag) Then
        IncludeFlag = rngIncludeFlag.Value
        iCount = 0
        For i = 1 To UBound(IncludeFlag, 1)
            If (IncludeFlag(i, 1) = True) Then
                iCount = iCount + 1
            End If
        Next i
        ReDim IncludePeriods(iCount, UBound(InPeriods, 2))
        ReDim IncludePrices(iCount, UBound(InPrices, 2))
        iCount = 0
        For i = 1 To UBound(IncludeFlag, 1)
            If (IncludeFlag(i, 1) = True) Then
                iCount = iCount + 1
                IncludePeriods(iCount, 1) = InPeriods(i, 1)
                IncludePeriods(iCount, 2) = InPeriods(i, 2)
                IncludePrices(iCount, 1) = InPrices(i, 1)
            End If
        Next i
        comp = msfc(tradedate, IncludePeriods, IncludePrices, Outperiods)
    Else
        comp = msfc(tradedate, InPeriods, InPrices, Outperiods)
    End If

End Function

Private Function msfc(tradedate As Date, InPeriods As Variant, InPrices As Variant, Outperiods) As Variant

Dim ta As Variant, tv As Variant, pv As Variant
Dim op As Variant
Dim Big_mat As Variant, H_mat As Variant, A_mat As Variant, b_vec As Variant
Dim Inv_mat As Variant, Sol_vec As Variant, Mul_vec As Variant
Dim xl_vec As Variant, coeff_vec As Variant
Dim m As Long, n As Long

'm: number of contracts
'n: number of splines
'j: spline j
    
    'Get the timevector from the Variant of Dates
    ta = gta(tradedate, InPeriods)
    op = gta(tradedate, Outperiods)
    tv = gtv(ta) ' Timevector knots.
    pv = gpv(InPrices)
    
    'TODO: Perform checks on dimensions and data values and types
    
    'QuickSort the time vector
    qsrt tv, LBound(tv), UBound(tv)
    
    'Remove duplicates from the timevector
    rd tv
    
    m = UBound(ta, 1)
    n = UBound(tv, 1) - 1
    
    H_mat = def_H(tv, n)
    A_mat = def_A(tv, ta, m, n)
    b_vec = def_b(pv, ta, m, n)
    Mul_vec = def_Mul_vec(b_vec, m, n)
    Big_mat = def_Big_Mat(H_mat, A_mat, m, n)
    'debugPrintVar BigMat, "BigMat_mat"
    
    'Inv_mat = RMatInvdll(Big_mat)
    Inv_mat = WorksheetFunction.MInverse(Big_mat)
    
    'Sol_vec = MATRIXMULTIPLY(Inv_mat, Mul_vec)
    Sol_vec = WorksheetFunction.MMult(Inv_mat, Mul_vec)
    msfc = Sol_vec
    
    'Retrieve x
    rxv Sol_vec, xl_vec, n
    'Reshape x
    coeff_vec = gca(xl_vec, n)
    
    msfc = gcp(tv, n, coeff_vec, op)
    'debugPrintVar A, "A_mat"
    'debugPrintVar H, "H_mat"
    'debugPrintVar b, "b_mat"
    
    'debugPrintVar InvMat, "InvMat_mat"
    'debugPrintVar MulVec, "Mul_vec"
    'debugPrintVar SolVec, "Sol_vec"
    
    
End Function

'Get Computed Prices
Private Function gcp(tv As Variant, n As Long, coeff As Variant, op As Variant) As Variant

Dim pdim As Long
Dim b As Double, e As Double, t1 As Double, t2 As Double
Dim i As Long, j As Long
Dim sumi As Double
Dim oc As Variant
    
    b = 0: e = 0: t1 = 0: t2 = 0
    pdim = UBound(op, 1)
    
    ReDim oc(pdim, 1)
    
    For i = 1 To pdim
        b = op(i, 1)
        e = op(i, 2)
        sumi = 0
        For j = 2 To n + 1
            If b < tv(j) And e > tv(j - 1) Then
                t1 = WorksheetFunction.Max(b, tv(j - 1))
                t2 = WorksheetFunction.Min(tv(j), e)
                sumi = sumi + F(t1, t2, coeff, j - 1)
            End If
        Next j
        oc(i, 1) = sumi / (e - b)
    Next i

    gcp = oc

End Function

Public Function F(t1 As Double, t2 As Double, coeff As Variant, j As Long)

Dim A As Double, b As Double, c As Double, d As Double, e As Double

    A = coeff(j, 1): b = coeff(j, 2): c = coeff(j, 3): d = coeff(j, 4): e = coeff(j, 5)

    F = (A * t2 ^ 5) / 5 + (b * t2 ^ 4) / 4 + (c * t2 ^ 3) / 3 + (d * t2 ^ 2) / 2 + e * t2 - _
        ((A * t1 ^ 5) / 5 + (b * t1 ^ 4) / 4 + (c * t1 ^ 3) / 3 + (d * t1 ^ 2) / 2 + e * t1)


End Function

'Retrieve solutionvector
Private Sub rxv(sv As Variant, x As Variant, n As Long)
Dim i As Long
Dim xdim As Long

    xdim = 5 * n
    
    ReDim x(xdim, 1)
    
    For i = 1 To xdim
        x(i, 1) = sv(i, 1)
    Next i

End Sub

Private Function def_Big_Mat(H As Variant, A As Variant, m As Long, n As Long) As Variant

Dim Big_mat As Variant
Dim i As Long, j As Long
Dim Hdim As Long, Adim As Long
    
    Hdim = 5 * n
    Adim = 3 * n + m - 2
    ReDim Big_mat(Adim + Hdim, Adim + Hdim)
    
    For i = 1 To Hdim + Adim
        For j = 1 To Hdim + Adim
            Big_mat(i, j) = 0#
        Next j
    Next i
    
    For i = 1 To Hdim
        For j = 1 To Hdim
            Big_mat(i, j) = H(i, j)
        Next j
    Next i
    
    For i = 1 To Adim
        For j = 1 To Hdim
                If (i > Hdim And j > Hdim) Then
                Else
                    Big_mat(i + Hdim, j) = A(i, j)
                    Big_mat(j, i + Hdim) = A(i, j)
                End If
        Next j
    Next i
    def_Big_Mat = Big_mat
    
End Function


Public Function def_Mul_vec(b As Variant, m As Long, n As Long) As Variant
Dim Mul_vec As Variant
Dim i As Long, j As Long
Dim bdim As Long, zdim As Long

    bdim = 3 * n + m - 2
    zdim = 5 * n
    
    ReDim Mul_vec(zdim + bdim, 1)
    
    
    For i = 1 To zdim
        Mul_vec(i, 1) = 0#
    Next i
    
    For j = 1 To bdim
        Mul_vec(zdim + j, 1) = b(j, 1)
    Next j
    def_Mul_vec = Mul_vec
End Function


Public Function def_b(pv As Variant, ta As Variant, m As Long, n As Long) As Variant
Dim i As Long, j As Long
Dim b_vec As Variant

    ReDim b_vec(3 * n + m - 2, 1)

    For i = 1 To 3 * n - 2
        b_vec(i, 1) = 0
    Next i
    
    For j = 1 To m
        b_vec(i - 1 + j, 1) = pv(j) * (ta(j, 2) - ta(j, 1))
    Next j
    
    def_b = b_vec
    
End Function

Public Function def_A(tv As Variant, ta As Variant, m As Long, n As Long) As Variant
Dim A_mat As Variant
Dim t1 As Double, t2 As Double
Dim i As Long, j As Long, z As Long
Dim rdim As Long, cdim As Long

    rdim = 3 * n + m - 2
    cdim = n * NUMCOEFF
    
    ReDim A_mat(rdim, cdim)
    
    z = 1
    
    For i = 1 To rdim
        For j = 1 To cdim
            A_mat(i, j) = 0#
        Next j
    Next i

    'Iterate splines
    For j = 2 To n ' Adjusted compared to BBK
        'Continuity of function at each knot:
        A_mat(z, (j - 2) * NUMCOEFF + APOS) = tv(j) ^ 4
        A_mat(z, (j - 1) * NUMCOEFF + APOS) = -tv(j) ^ 4
        A_mat(z, (j - 2) * NUMCOEFF + BPOS) = tv(j) ^ 3
        A_mat(z, (j - 1) * NUMCOEFF + BPOS) = -tv(j) ^ 3
        A_mat(z, (j - 2) * NUMCOEFF + CPOS) = tv(j) ^ 2
        A_mat(z, (j - 1) * NUMCOEFF + CPOS) = -tv(j) ^ 2
        A_mat(z, (j - 2) * NUMCOEFF + DPOS) = tv(j)
        A_mat(z, (j - 1) * NUMCOEFF + DPOS) = -tv(j)
        A_mat(z, (j - 2) * NUMCOEFF + EPOS) = 1
        A_mat(z, (j - 1) * NUMCOEFF + EPOS) = -1
        z = z + 1
        'Continuity of first derivative at each knot:
        A_mat(z, (j - 2) * NUMCOEFF + APOS) = 4 * tv(j) ^ 3
        A_mat(z, (j - 1) * NUMCOEFF + APOS) = -4 * tv(j) ^ 3
        A_mat(z, (j - 2) * NUMCOEFF + BPOS) = 3 * tv(j) ^ 2
        A_mat(z, (j - 1) * NUMCOEFF + BPOS) = -3 * tv(j) ^ 2
        A_mat(z, (j - 2) * NUMCOEFF + CPOS) = 2 * tv(j)
        A_mat(z, (j - 1) * NUMCOEFF + CPOS) = -2 * tv(j)
        A_mat(z, (j - 2) * NUMCOEFF + DPOS) = 1
        A_mat(z, (j - 1) * NUMCOEFF + DPOS) = -1
        z = z + 1
        'Continuity of second derivative at each knot:
        A_mat(z, (j - 2) * NUMCOEFF + APOS) = 12 * tv(j) ^ 2
        A_mat(z, (j - 1) * NUMCOEFF + APOS) = -12 * tv(j) ^ 2
        A_mat(z, (j - 2) * NUMCOEFF + BPOS) = 6 * tv(j)
        A_mat(z, (j - 1) * NUMCOEFF + BPOS) = -6 * tv(j)
        A_mat(z, (j - 2) * NUMCOEFF + CPOS) = 2
        A_mat(z, (j - 1) * NUMCOEFF + CPOS) = -2
        z = z + 1
    Next j
 
    'End Condition
    A_mat(z, (n - 1) * NUMCOEFF + APOS) = 4 * tv(n + 1) ^ 3
    A_mat(z, (n - 1) * NUMCOEFF + BPOS) = 3 * tv(n + 1) ^ 2
    A_mat(z, (n - 1) * NUMCOEFF + CPOS) = 2 * tv(n + 1)
    A_mat(z, (n - 1) * NUMCOEFF + DPOS) = 1
    
    z = z + 1
    
    'Set up the integral constraints
    'Integral function = integral of prices
    For i = 1 To m
        For j = 2 To n + 1
            If (ta(i, 2) > tv(j - 1) And ta(i, 1) < tv(j)) Then
                t1 = WorksheetFunction.Max(ta(i, 1), tv(j - 1))
                t2 = WorksheetFunction.Min(tv(j), ta(i, 2))
                A_mat(z, (j - 2) * NUMCOEFF + APOS) = 0.2 * (t2 ^ 5 - t1 ^ 5)
                A_mat(z, (j - 2) * NUMCOEFF + BPOS) = 0.25 * (t2 ^ 4 - t1 ^ 4)
                A_mat(z, (j - 2) * NUMCOEFF + CPOS) = (1 / 3) * (t2 ^ 3 - t1 ^ 3)
                A_mat(z, (j - 2) * NUMCOEFF + DPOS) = 0.5 * (t2 ^ 2 - t1 ^ 2)
                A_mat(z, (j - 2) * NUMCOEFF + EPOS) = (t2 - t1)
            End If
        Next j
        z = z + 1
    Next i
 
 def_A = A_mat
    
End Function

Public Function def_H(tv As Variant, n As Long) As Variant

Dim H_mat As Variant
Dim z As Long, i As Long, j As Long

ReDim H_mat(n * NUMCOEFF, n * NUMCOEFF)

For i = 1 To n * NUMCOEFF
    For j = 1 To n * NUMCOEFF
        H_mat(i, j) = 0
    Next j
Next i

z = 1

For j = 2 To n + 1
        H_mat(z, z) = 2 * (144 / 5) * (tv(j) - tv(j - 1)) ^ 5
        H_mat(z, z + 1) = 2 * 18 * (tv(j) - tv(j - 1)) ^ 4
        H_mat(z, z + 2) = 2 * 8 * (tv(j) - tv(j - 1)) ^ 3
        H_mat(z + 1, z) = 2 * 18 * (tv(j) - tv(j - 1)) ^ 4
        H_mat(z + 1, z + 1) = 2 * 12 * (tv(j) - tv(j - 1)) ^ 3
        H_mat(z + 1, z + 2) = 2 * 6 * (tv(j) - tv(j - 1)) ^ 2
        H_mat(z + 2, z) = 2 * 8 * (tv(j) - tv(j - 1)) ^ 3
        H_mat(z + 2, z + 1) = 2 * 6 * (tv(j) - tv(j - 1)) ^ 2
        H_mat(z + 2, z + 2) = 2 * 4 * (tv(j) - tv(j - 1))
        z = z + 5
Next j

def_H = H_mat

End Function

'Get time array
Public Function gta(tradedate As Date, ByRef PeriodData As Variant) As Variant
Dim i As Long, n As Long

Dim tv As Variant

    n = UBound(PeriodData, 1)
    ReDim tv(n, 2)
    
    For i = 1 To n
        tv(i, 1) = (PeriodData(i, 1) - tradedate) / 365
        tv(i, 2) = (PeriodData(i, 2) - tradedate) / 365
    Next i
    
    gta = tv

End Function

'Get Coefficient array
Private Function gca(x As Variant, n As Long) As Variant
Dim xdim As Long, cdim As Long
Dim i As Long
Dim ca As Variant

ReDim ca(n, 5)

For i = 1 To UBound(x, 1)
    ca(Int((i - 1) / 5) + 1, (i - 1) Mod 5 + 1) = x(i, 1)
Next i

gca = ca
End Function

'Get time vector
Private Function gtv(ByRef ta As Variant) As Variant
Dim i As Long, n As Long

Dim tv As Variant

    n = UBound(ta, 1) * 2
    ReDim tv(n)
    
    For i = 1 To n
        tv(i) = ta(Int((i + 1) / 2), ((i + 1) Mod 2) + 1)
    Next i
    
    gtv = tv

End Function

'Get time vector
Public Function gpv(ByRef PriceData As Variant) As Variant
Dim i As Long, n As Long

Dim pv As Variant

    n = UBound(PriceData, 1)
    ReDim pv(n)
    
    For i = 1 To n
        pv(i) = PriceData(i, 1)
    Next i
    
    gpv = pv

End Function
